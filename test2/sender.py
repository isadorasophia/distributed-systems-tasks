"""
    Sender class:
        Simulates a process sending a rumor to N different host/ports:
            -> Keep sending rumors until a signal is sent
            -> Return total messages sent as a result
"""

import random
import threading, Queue
import zmq

from structures import *
from helpers import *

class SenderProcess(threading.Thread):
    """
        Emulate a process, which is responsible for gossiping.
        > SEND STUFF!
            process:    information of current process
            msg:        msg to be sent
            q:          queue to sync data
    """
    def __init__(self, process, msg, queue):
        self.p = process
        self.msg = msg

        self.q = queue

        # total of messages sent
        self.total_sent = 0

        self.random = random.Random()
        random.seed(self.p.port)

        self.terminate = False
        threading.Thread.__init__(self)

    def run(self):
        try:
            # set our socket to begin our send process!
            sender_socket = self.p.context.socket(zmq.PUSH)
        except:
            if __debug__:
                print '[@] EXCEPTION AT SENDER: ' + str(self.p.port)

            return

        # prepare our payload as well
        payload = Payload(self.p.host, self.p.port)
        payload.set_msg(self.msg)

        processes = list(self.p.host_list.items())

        # keep sending to anyone who listens
        while not self.terminate:
            random_ip, (min_port, max_port) = self.random.choice(processes)
            random_port = self.random.randint(min_port, max_port)

            # if something went wrong
            if send(sender_socket, random_ip, random_port, payload) == -1:
                break

            self.total_sent += 1

        # apply result        
        self.q.put(self.total_sent)

        # clean up!
        sender_socket.close(linger=0)

        return
