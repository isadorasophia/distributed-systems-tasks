"""
    Helper methods for gossip simulation
"""

import time
import zmq

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
        time.sleep(.5)

        return 1

    except:
        print '# Send process was interrupted!'
        return -1

def range_n(n, start, end, exclude=False):
    """
        Produces a range from start to end, without n
    """
    if exclude:
        return range(start, n) + range(n+1, end)
    else:
        return range(start, end)

def miliseconds():
    return int(round(time.time() * 1000))