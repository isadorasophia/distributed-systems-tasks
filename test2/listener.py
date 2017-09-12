"""
    Listener class:
        Simulates a process receiving rumors;
            -> If rumor is new, dispatch a SENDER thread for the process
            -> else if is already received, send a STOP reply
            -> If received a STOP message from another process, check if it needs to stop 
               sending new rumors
            -> Return total messages sent&total rumors received as a result
"""

import random
import threading, Queue
import zmq

from sender import SenderProcess

from structures import *
from helpers import *

class ListenerProcess(threading.Thread):
    """
        Emulate a process, which is responsible for gossiping.
        > LISTEN STUFF!
            q:          shared queue with process information
            k:          chance of a process to stop
    """
    def __init__(self, q, k, res):
        # get current PROCESS information
        self.q = q
        self.p = self.q.get()
        self.res = res

        # STATISTICS:
        self.rumor_attempts = 0
        self.total_rumors_recv = 0

        self.endpoint = tcp_endpoint(self.p.host, self.p.port)
        self.context = self.p.context
        self.sender = None

        self.k = k * 1.
        self.all_msg = set()

        self.random = random.Random()
        random.seed(self.p.port)

        threading.Thread.__init__(self)
        self.terminate = False
        # self.daemon = True

    def run(self):
        try:
            recv_socket = self.context.socket(zmq.PULL)     # PULL SOCKET
            recv_socket.setsockopt(zmq.LINGER, 0)           # just in case: do not linger
            recv_socket.setsockopt(zmq.RCVTIMEO, 90000)     # apply a timeout of 1m30s
            recv_socket.set_hwm(100000)                     # buffer for stack size
            recv_socket.bind(self.endpoint)                 # CONNECT

            sender_socket = self.context.socket(zmq.PUSH)   # PUSH SOCKET
        except:
            # just go away, process FAILED
            self.q.task_done()

            if __debug__:
                print '[@] EXCEPTION AT LISTENER: ' + str(self.p.port)
            return

        # keeps listening to any messages
        while self.terminate is False:
            if __debug__:
                print '[\] PORT: ' + str(self.p.port) + ', QUEUE L: ' + str(self.q.unfinished_tasks)

            # if we are ALREADY done 
            #    -> give priority to process that aren't done yet
            if self.sender is not None and self.sender.terminate:
                time.sleep(1)

            try:
                msg = recv_socket.recv_pyobj()
            except:
                # if context was terminated OR:
                #   - if expired timeout and we have never received any message, just assume that
                #   the thread will never receive any message
                #   - otherwise, it's just messing with our priority system and go away
                if self.sender is None or self.sender.terminate == False:
                    self.res.put((-1, -1))
                    self.q.task_done()

                    return

                break

            ## REQUEST
            if msg.req:
                # have we already received it?
                if msg.content in self.all_msg:
                    # create a reply telling the source to stop
                    rep = Payload(self.p.host, self.p.port)
                    rep.set_stop()

                    send(sender_socket, msg.host, msg.port, rep)

                else:
                    if __debug__:
                        print '[*] MESSAGE RECEIVED: \t' + str(self.p.port)

                    # get this message done, start dispatcher
                    self.all_msg.add(msg.content)
                    self.sender_q = Queue.Queue()

                    # by now: we can only handle one message (a.k.a. do NOT dispatch another sender)
                    assert(self.sender is None)

                    self.sender = SenderProcess(process=self.p, msg=msg.content, queue=self.sender_q)
                    self.sender.start()

                self.total_rumors_recv += 1

            ## REPLY
            else:
                if msg.stop:
                    if self.stop():
                        # if we didn't have a sender, it just doesn't make sense!
                        assert(self.sender is not None)

                        # have we terminated it yet?
                        if self.sender.terminate is False:
                            self.sender.terminate = True
                            self.q.task_done()

                            if __debug__:
                                print '[$] SHUT DOWN: \t' + str(self.p.port)

        # clean up!
        self.sender.terminate = True
        self.res.put((self.sender_q.get(), self.total_rumors_recv))

        try:
            sender_socket.close(linger=0)
            recv_socket.close(linger=0)
        except:
            if __debug__:
                print '[X] CLOSED: \t' + str(self.p.port)

        return

    def stop(self):
        """
            Chance of 1/k in stopping the thread
        """
        return self.random.uniform(0, 1) < 1/self.k
