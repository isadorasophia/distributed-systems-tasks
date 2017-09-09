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

def tcp_endpoint(ip, port):
    return "tcp://" + ip + ":" + str(port)

class SenderProcess(threading.Thread):
    """
        Emulate a process, which is responsible for gossiping.
        > SEND STUFF!
            q:          shared queue
            context:    zmq context
            host&port:  communication info
            n:          total of processes
            min_port:   minimum port available
    """
    def __init__(self, context, host, port, msg,
                    n, min_port=5000):
        self.context = context
        self.n = n
        self.min_port = min_port

        self.host = host
        self.port = port
        self.msg = msg

        self.random = random.Random()
        random.seed(port)

        self.stop = False
        threading.Thread.__init__(self)

    def run(self):
        payload = Payload(self.host, self.port)
        payload.set_msg(self.msg)

        # keep sending to anyone who listens
        while not self.stop:
            random_ip = "localhost"
            random_port = self.random.randint(min_port, n)

            send(random_ip, random_port, payload)

class ListenerProcess(threading.Thread):
    """
        Emulate a process, which is responsible for gossiping.
        > LISTEN STUFF!
            q:          shared queue
            context:    zmq context
            ip&port:    communication info
            n:          total of processes
            k:          chance of a process to stop
            min_port:   minimum port available
    """
    def __init__(self, q, context, host, port,
                    n, k, min_port=5000):
        # shared variables
        self.q = q
        self.q.get()

        self.context = context
        self.host = host
        self.port = port

        self.n = n
        self.k = k * 1.

        self.random = random.Random()
        random.seed(port)
        self.all_msg = set()

        self.sender = None

        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        recv_socket = self.context.socket(zmq.PULL)
        recv_socket.bind(tcp_endpoint(self.host, self.port))

        # keeps listening to any messages
        while True:
            msg = pickle.loads(recv_socket.recv())

            ## REQUEST
            if msg.req:
                # have we already received it?
                if msg.content in self.all_msg:

                    # create a reply telling this sender to stop
                    rep = Payload(ip, port)
                    rep.set_stop()

                    # connect to whoever sent me
                    self.send(msg[ip], msg[port], rep)

                else:
                    # get this message done, start dispatcher
                    self.all_msg.add(msg.content)

                    # we can only handle one message, by now
                    assert(self.sender is None)

                    self.sender = SenderProcess(self.context, self.host, self.port, \
                        msg.content, self.n, self.min_port)

                    self.sender.start()

            ## REPLY
            else:
                if msg.stop:
                    if self.stop():
                        # if we don't have a sender, it doesn't make sense
                        assert(self.sender is not None)

                        self.sender.stop = True
                        self.q.task_done()

                    ## else just ignores: can't stop, won't stop

                ## else just ignores: it's a happy reply

    def stop(self):
        """
            Chance of 1/k in stopping the thread
        """
        return self.random.uniform(0, 1) < 1/self.k

    def send(self, ip, port, payload):
        """
            Send a payload to an ip and port through TCP
        """
        s = self.context.socket(zmq.PUSH)
        s.connect(tcp_endpoint(ip, port))

        s.send(picke.dumps(payload))

def cook_parser():
    """
        Returns a parser dedicated to our GOSSIP simulation.
    """
    parser = argparse.ArgumentParser(description='Gossip protocol simulation.')

    parser.add_argument('n', metavar='N', type=int, help='total of processes')
    parser.add_argument('k', metavar='K', type=int, help='probability to stop (i.e.: p < 1/K)')

    return parser

def main(N, K):
    min_port = 5000
    max_port = 50000

    ip = "127.0.0.1"

    # we can't surpass our limit
    assert(min_port + N < max_port)

    # context variables
    context = zmq.Context()
    context.set(zmq.MAX_SOCKETS, N)
    q = Queue.Queue()

    for i in xrange(N):
        q.put(i)
        process = ListenerProcess(q, context, ip, min_port+i,
                    N, K, min_port)
        process.start()

    # wait for all process to be done
    q.join()

if __name__ == "__main__":
    parser = cook_parser()
    args = parser.parse_args()

    main(args.n, args.k)
