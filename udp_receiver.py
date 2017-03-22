import socket
import struct
import sys

from CommandTree import CommandTree, AsterixNode

MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

floor = sys.argv[0]
room = sys.argv[1]

cmdTree = CommandTree()
cmdTree.execute_command("*;1;change")

""""
while True:
    command = sock.recv(10240)
    cmd_parts = command.split(';')
    print cmd_parts
    conditions = [room == cmd_parts[1], room == "*", floor == cmd_parts[0],floor == "*"]
    if reduce(lambda x,y: x or y, conditions):
        pass
"""

