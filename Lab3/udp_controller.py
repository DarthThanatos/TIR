#!/usr/bin/env python

import socket

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)    



def send(line):
    print 'SENT: "%s"' % line
    sock.sendto(line, (MCAST_GRP, MCAST_PORT))

def listen_to_hardware():
    pass

def listen_to_software():
    cmd = raw_input("Type command to send in format [floor];[room];[device];[ID];[operation]: \n")
    send(cmd)

while True:
    line = raw_input('Prompt ("q" to quit, "h" to listen to hardware, "s" to listen to software): \n')
    if line == 'q':
        break
    if line == 'h':
        listen_to_hardware()
    elif line == 's':
        listen_to_software()
    else:
        print "Not a valid option"
        continue
