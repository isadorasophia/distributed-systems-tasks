"""
    Helper structures for gossip simulation
"""

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