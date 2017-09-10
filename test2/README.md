## Report for test 2

_Student: Isadora Sophia Garcia Rodopoulos_

_RA: 158018_

### Intro
The assignment proposed the simulation of the gossip protocol, by relying on TCP/IP sockets. 

```
python [-O] gossip.py N K
```

In summary, the algorithm consisted in:

* ```N``` and ```k``` were received as arguments;
* dispatch a total of ```N``` processes, each with its own port;
* send a single message as a *rumor* for the first process;
* for each process:
     + a _listener_ is created and awaits for a rumor
     + when a rumor is received for the first time, starts a _sender_: which spreads the rumor randomly accross all processes available
     + if _listener_ received another rumor, it sends a *STOP* message back.
     + otherwise, if it received a *STOP* message, stops sending new messages with a probability of ```1/k```
        + if ```p < 1/k```, interrupts _sender_, sends a signal and continues to listen for new messages
* when all processes have received the rumor, stop the application and gather data 
* otherwise, force quit the application

### Implementation
The implementation relied on the _ZeroMQ_ library in _Python_ - mainly due to the complexity of the packets and to allow shorter feedbacks, even though it was initially implemented in _C_.

Each process is dispatched as a thread, using ```threading``` library from _Python_ - i.e. a _listener_ and a _sender_ are two different threads, related to a same abstract process, bound to a certain port.

### Results
The results turned out to be highly experimental. For instance, in order to allow its execution on my OS (Ubuntu 16.04), some flags configuration were necessary, such as:

```
ulimit -n
ulimit -s
cat /etc/security/limits.conf
sysctl -n fs.nr_open
```

These commands allowed to increase the limit of total of sockets supported by the OS and the stack size per application, which were necessary specially when N > 1000.

#### How many times did each process tried to gossip?
    ![Graph]()

#### What was the parcel of successfull gossip attempts?

#### In the end of the dissemination, how many process have the rumor?

#### How long did it take betwewen the start and the end of the dissemination?

### Extra
Through _Azure_ virtual machines, it was executed a test of the application between more than two hosts.
