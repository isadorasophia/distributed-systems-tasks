## Report for test 2

_Student: Isadora Sophia Garcia Rodopoulos_

_RA: 158018_

### Intro
The assignment consisted in simulating the gossip protocol relying on TCP/IP sockets.

* the application receives an input ```N``` and ```k``` as argument;
* dispatch a total of N processes, each with its own port
* send a message as a rumor
* for each process:
     + a _listener_ is created and awaits for a *rumor*
     + when a rumor is received, starts a _sender_, which spreads the rumor randomly accross all processes available
     + if _listener_ receives another rumor, send a *STOP* message back.
     + otherwise, if it receives a *STOP* message, stops sending new messages with a probability of 1/k
        + if stops sending the message, send a signal and continue to listen for new messages
* when all processes have received the message, stop the application and gather data -> otherwise, force quit the application

### Implementation
The implementation relied on the _ZeroMQ_ library in _Python_ - due mainly to the complexity of the packets and to allow shorter feedbacks, even though it was initially implemented in _C_.

Each process is dispatched as a thread, using ```threading``` library from _Python_ - i.e. a _listener_ and a _sender_ are two different threads, related to a same abstract process, bound to a certain port.

### Results
The results turned out to be highly experimental. For instance, in order to allow its execution on my OS (Ubuntu 16.04), some flags setting were necessary, such as:

```
ulimit -n
ulimit -s
cat /etc/security/limits.conf
sysctl -n fs.nr_open
```

The following commands allowed to increase the limit of total of sockets supported by the OS and the stack size per application, which were necessary specially when N > 1000.

1. How many times did each process tried to gossip?
    ![Graph]()

2. What was the parcel of successfull gossip attempts?

3. In the end of the dissemination, how many process have the rumor?

4. How long did it take betwewen the start and the end of the dissemination?

### Extra
Through _Azure_ virtual machines, it was executed a test of the application between more than two hosts.