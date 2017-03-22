#!/usr/bin/env python

import socket

MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)    



def send(line):
    print 'SENT: "%s"' % line
    sock.sendto(line, (MCAST_GRP, MCAST_PORT))

def listen_to_hardware():
    pass

def listen_to_software():
    pass

while True:
    line = raw_input('Prompt ("stop" to quit, "h" to listen to hardware, "s" to listen to software): ')
    if line == 'stop':
        break
    if line == 'h':
        listen_to_hardware()
    elif line == 's':
        listen_to_software()
    else:
        continue
