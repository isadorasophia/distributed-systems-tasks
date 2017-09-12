"""
    Simulation of gossip protocol using ZMQ API
        Author: Isadora Sophia Garcia Rodopoulos
"""

import argparse, time, sys
import threading, Queue
import zmq

from structures import *
from helpers import *

from listener import ListenerProcess

def main(N, K):
    """
        Main function!
    """

    #### definitions
    min_port = 15000
    max_port = 50000

    host_list = {"127.0.0.1": (min_port, min_port+N-1)}
    current_ip = "127.0.0.1"

    msg = "Very important and high priority message."

    # we can't surpass our limit
    assert(min_port + N < max_port)

    #### context variables
    context = zmq.Context()
    context.set(zmq.MAX_SOCKETS, N*3+1)
    context.setsockopt(zmq.LINGER, 1)    # OBS: linger does not work for multiple hosts!

    q = Queue.Queue()
    listeners = []
    res = []

    #### start time!
    start = miliseconds()

    ## start our listeners!
    for i in xrange(N):
        # create a new process as a LISTENER
        q.put(Process(context, current_ip, min_port+i, host_list))

        res.append(Queue.Queue())
        listeners.append(ListenerProcess(q, K, res[i]))

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

    #### time is over!
    end = miliseconds()

    ### end all processes
    for i in xrange(N):
        listeners[i].terminate = True

    context.term()

    ### gather data
    min_sent        = sys.maxint
    max_sent        = 0
    total_sent      = 0
    total_failed    = 0
    received        = 0.
    total_sent_i    = [0] * N

    for i in xrange(N):
        total_sent_i[i], failed = res[i].get()

        # skip failed tests
        if failed == -1:
            continue
        else:
            received += 1

        total_failed += failed-1

        total_sent += total_sent_i[i]
        if total_sent_i[i] < min_sent:
            min_sent = total_sent_i[i]

        if total_sent_i[i] > max_sent:
            max_sent = total_sent_i[i]

    print '\n############# Results report:'
    print 'Min. sent from p.: \t'   + str(min_sent)
    print 'Max. sent from p.: \t'   + str(max_sent)
    print 'Total sent: \t\t'        + str(total_sent)
    print 'Average per p.: \t'      + str(total_sent/received)
    print 'Total failed rumors: \t' + str(total_failed)
    print 'P. with rumor: \t\t'     + str(int(received)) + '/' + str(N)

    if total_sent != 0:
        print 'Rate Failed/Success: \t' + str(total_failed/(total_sent*1.))
    else:
        print 'Rate Failed/Success: \t#'

    print 'Time: \t\t\t' + str(end-start) + 'ms'

    return

def cook_parser():
    """
        Returns a parser dedicated to our Gossip simulation.
    """
    parser = argparse.ArgumentParser(description='Gossip protocol simulation.')

    parser.add_argument('n', metavar='N', type=int, help='total of processes')
    parser.add_argument('k', metavar='K', type=int, help='probability to stop (i.e.: p < 1/K)')

    return parser

if __name__ == "__main__":
    parser = cook_parser()
    args = parser.parse_args()

    main(args.n, args.k)
