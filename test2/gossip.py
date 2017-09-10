"""
    Simulation of gossip protocol using ZMQ API
        Author: Isadora Sophia Garcia Rodopoulos
"""

import argparse, random, time, sys
import threading, Queue
import zmq

class Payload:
    """
        Skeleton of a payload responsible for exchange of 
        messages in gossip protocol
          host&port:    origin address 
          req:          if current message is a REQ with a message
          stop:         should we tell a process to be stopped?
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.req = False 
        self.stop = False

    def set_msg(self, msg):
        self.content = msg
        self.req = True

    def set_stop(self):
        self.stop = True

class Process:
    """
        Basic info. regarding a process 
          context:      ZMQ context
          ip&port:      communication info
          host_list:    all hosts available and its respective ports
    """
    def __init__(self, context, host, port, host_list):
        self.context = context
        self.host_list = host_list

        self.host = host 
        self.port = port

class SenderProcess(threading.Thread):
    """
        Emulate a process, which is responsible for gossiping.
        > SEND STUFF!
            process:    information of current process
            msg:        msg to be sent
    """
    def __init__(self, process, msg):
        self.p = process
        self.msg = msg

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

            send(sender_socket, random_ip, random_port, payload)

            self.total_sent += 1
            if __debug__:
                print '[/] MSG TO: ' + str(random_port) + ', FROM: ' + str(self.p.port)

        # clean up!
        sender_socket.close(linger=0)

        return

class ListenerProcess(threading.Thread):
    """
        Emulate a process, which is responsible for gossiping.
        > LISTEN STUFF!
            q:          shared queue with process information
            k:          chance of a process to stop
    """
    def __init__(self, q, k):
        # get current PROCESS information
        self.q = q
        self.p = self.q.get()

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

            try:
                msg = recv_socket.recv_pyobj()
            except zmq.ContextTerminated:
                # it means that things are done, just go away
                return

            ## REQUEST
            if msg.req:
                # have we already received it?
                if msg.content in self.all_msg:

                    # create a reply telling this sender to stop
                    rep = Payload(self.p.host, self.p.port)
                    rep.set_stop()

                    send(sender_socket, msg.host, msg.port, rep)

                else:
                    if __debug__:
                        print '[*] MESSAGE RECEIVED: \t' + str(self.p.port)

                    # get this message done, start dispatcher
                    self.all_msg.add(msg.content)

                    # by now: we can only handle one message (a.k.a. do NOT dispatch another sender)
                    assert(self.sender is None)

                    self.sender = SenderProcess(process=self.p, msg=msg.content)
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

                            self.rumor_attempts += self.sender.total_sent

                            if __debug__:
                                print '[$] SHUT DOWN: \t' + str(self.p.port)

            # if we are ALREADY done 
            #    -> give priority to process that aren't done yet
            if self.sender is not None and self.sender.terminate:
                time.sleep(1)

        # clean up!
        sender_socket.close(linger=0)
        recv_socket.close(linger=0)

        return

    def stop(self):
        """
            Chance of 1/k in stopping the thread
        """
        return self.random.uniform(0, 1) < 1/self.k

################### Helper functions! ###################

def cook_parser():
    """
        Returns a parser dedicated to our Gossip simulation.
    """
    parser = argparse.ArgumentParser(description='Gossip protocol simulation.')

    parser.add_argument('n', metavar='N', type=int, help='total of processes')
    parser.add_argument('k', metavar='K', type=int, help='probability to stop (i.e.: p < 1/K)')

    return parser

def tcp_endpoint(ip, port):
    """
        Create a TCP endpoint string
    """
    return "tcp://" + ip + ":" + str(port)

def send(socket, ip, port, payload):
    """
        Send a payload to an ip and port through TCP, using ZMQ sockets
    """
    endpoint = tcp_endpoint(ip, port)

    try:
        socket.connect(endpoint)
        socket.send_pyobj(payload, flags=zmq.NOBLOCK)

        socket.disconnect(endpoint)
        time.sleep(.05)

    except:
        print '# Send process was interrupted!'
        return

def miliseconds():
    return int(round(time.time() * 1000))

def main(N, K):
    """
        Main function!
    """

    # DEFINITIONS
    min_port = 15000
    max_port = 50000

    host_list = {"127.0.0.1": (min_port, min_port+N-1)}
    current_ip = "127.0.0.1"

    msg = "Very important and high priority message."

    # we can't surpass our limit
    assert(min_port + N < max_port)

    # context variables
    context = zmq.Context()
    context.set(zmq.MAX_SOCKETS, N*3+1)
    context.setsockopt(zmq.LINGER, 1)

    q = Queue.Queue()
    listeners = []

    start = miliseconds()

    for i in xrange(N):
        # create a new process as a LISTENER
        q.put(Process(context, current_ip, min_port+i, host_list))
        listeners.append(ListenerProcess(q, K))

        listeners[i].start()

    ## begin to spread rumor!
    if current_ip == host_list.keys()[0]:
        print '[!] Sending first message: ' + msg

        sender_socket = context.socket(zmq.PUSH)
        payload = Payload(current_ip, min_port)
        payload.set_msg(msg)

        send(sender_socket, current_ip, min_port, payload)
        sender_socket.close()

    # wait for all process to be done
    q.join()

    end = miliseconds()

    min_sent = sys.maxint
    max_sent = 0
    total_sent = 0
    total_failed = 0

    total_sent_i = [0] * N

    for i in xrange(N):
        listeners[i].terminate = True

        total_sent_i[i] = listeners[i].rumor_attempts
        total_failed += listeners[i].total_rumors_recv-1

        total_sent += total_sent_i[i]
        if total_sent_i[i] < min_sent:
            min_sent = total_sent_i[i]

        if total_sent_i[i] > max_sent:
            max_sent = total_sent_i[i]

    context.term()

    print min_sent
    print max_sent
    print total_sent
    print total_failed
    print end-start

    return

if __name__ == "__main__":
    parser = cook_parser()
    args = parser.parse_args()

    main(args.n, args.k)
