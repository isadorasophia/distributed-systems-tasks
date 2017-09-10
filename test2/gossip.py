import argparse, pickle, random
import threading, Queue
import zmq

class Payload:
    """
        Skeleton of a payload responsible for exchange of 
        messages in gossip protocol
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.req = False    # if current message is REQ or REP
        self.stop = False   # tell process to stop or not

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

        self.random = random.Random()
        random.seed(self.p.port)

        self.terminate = False
        threading.Thread.__init__(self)

    def run(self):
        # prepare our socket and payload to begin send process!
        try:
            sender_socket = self.p.context.socket(zmq.PUSH)
        except:
            print('[@] EXCEPTION AT: ' + str(self.p.port))
            return

        payload = Payload(self.p.host, self.p.port)
        payload.set_msg(self.msg)

        processes = list(self.p.host_list.items())

        # keep sending to anyone who listens
        while not self.terminate:
            random_ip, (min_port, max_port) = self.random.choice(processes)
            random_port = self.random.randint(min_port, max_port)

            print 'CHOOSE ' + str(random_port)

            send(sender_socket, random_ip, random_port, payload)

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
        self.endpoint = tcp_endpoint(self.p.host, self.p.port)

        self.context = self.p.context
        self.k = k * 1.

        self.all_msg = set()
        self.sender = None

        self.random = random.Random()
        random.seed(self.p.port)

        threading.Thread.__init__(self)
        self.terminate = False
        #self.daemon = True

    def run(self):
        try:
            recv_socket = self.context.socket(zmq.PULL)
            recv_socket.setsockopt(zmq.LINGER, 0)
            recv_socket.set_hwm(100000)
            recv_socket.bind(self.endpoint)

            sender_socket = self.context.socket(zmq.PUSH)
        except:
            # just go away, process FAILED
            self.q.task_done()

            print('[@] PROCESS TERMINATED: \t' + self.endpoint)
            return

        # keeps listening to any messages
        while self.terminate is False:
            print str(self.p.port) + ' AND QUEUE L: ' + str(self.q.unfinished_tasks)
            try:
                if self.q.unfinished_tasks < 1:
                    msg = pickle.loads(recv_socket.recv(flags=zmq.NOBLOCK))
                else:
                    msg = pickle.loads(recv_socket.recv())
            except zmq.ContextTerminated:
                print('[@] PROCESS TERMINATED: \t' + self.endpoint)
                return
            except zmq.Again:
                print('port: ' + str(self.p.port))
                continue

            ## REQUEST
            if msg.req:
                # have we already received it?
                if msg.content in self.all_msg:

                    # create a reply telling this sender to stop
                    rep = Payload(self.p.host, self.p.port)
                    rep.set_stop()

                    # connect to whoever sent me
                    send(sender_socket, msg.host, msg.port, rep)

                else:
                    print('[$] MESSAGE RECEIVED: \t' + str(self.p.port))

                    # get this message done, start dispatcher
                    self.all_msg.add(msg.content)

                    # we can only handle one message, by now
                    assert(self.sender is None)

                    self.sender = SenderProcess(process=self.p, msg=msg.content)
                    self.sender.start()

            ## REPLY
            else:
                if msg.stop:
                    if self.stop():
                        # if we don't have a sender, it doesn't make sense
                        assert(self.sender is not None)

                        if self.sender.terminate is False:
                            self.sender.terminate = True

                            print('[$] SHUT DOWN: \t' + str(self.p.port))
                        
                            self.q.task_done()
                            sender_socket.close(linger=0)
                            recv_socket.close(linger=0)
                            return

                    ## else just ignores: can't stop, won't stop

                ## else just ignores: it's a happy reply

        return

    def stop(self):
        """
            Chance of 1/k in stopping the thread
        """
        return self.random.uniform(0, 1) < 1/self.k

################### Helper functions! ###################

def cook_parser():
    """
        Returns a parser dedicated to our GOSSIP simulation.
    """
    parser = argparse.ArgumentParser(description='Gossip protocol simulation.')

    parser.add_argument('n', metavar='N', type=int, help='total of processes')
    parser.add_argument('k', metavar='K', type=int, help='probability to stop (i.e.: p < 1/K)')

    return parser

def tcp_endpoint(ip, port):
    """
        Bake a TCP endpoint string
    """
    return "tcp://" + ip + ":" + str(port)

def send(socket, ip, port, payload):
    """
        Send a payload to an ip and port through TCP, using ZMQ sockets
    """
    endpoint = tcp_endpoint(ip, port)

    try:
        socket.connect(endpoint)
        socket.send(pickle.dumps(payload), flags=zmq.NOBLOCK)

        socket.disconnect(endpoint)

    except:
        print('# Send process was interrupted')
        return

def main(N, K):
    """
        Main function!
    """
    current_ip = "127.0.0.1"
    msg = "Very important and high priority message."

    min_port = 15000
    max_port = 50000

    # we can't surpass our limit
    assert(min_port + N < max_port)

    host_list = {"127.0.0.1": (min_port, min_port+N-1)}

    # context variables
    context = zmq.Context()
    context.set(zmq.MAX_SOCKETS, N*3+1)
    context.setsockopt(zmq.LINGER, 1)

    q = Queue.Queue()
    listeners = []

    for i in xrange(N):
        q.put(Process(context, current_ip, min_port+i, host_list))
        listeners.append(ListenerProcess(q, K))
        listeners[i].start()

    ## begin to spread rumor!
    if current_ip == host_list.keys()[0]:

        print('[!] Sending first message: ' + msg)

        sender_socket = context.socket(zmq.PUSH)
        payload = Payload(current_ip, min_port)
        payload.set_msg(msg)

        send(sender_socket, current_ip, min_port, payload)
        sender_socket.close()

    # wait for all process to be done
    q.join()

    for i in xrange(N):
        listeners[i].terminate = True

    context.term()
    return

if __name__ == "__main__":
    parser = cook_parser()
    args = parser.parse_args()

    main(args.n, args.k)
