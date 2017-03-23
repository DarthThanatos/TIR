import socket
import struct
import sys

from CommandTree import CommandTree, AsterixNode

MCAST_GRP = '236.0.0.0'
MCAST_PORT = 3456

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
sock.settimeout(3)
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

floor = sys.argv[1]
room = sys.argv[2]

cmdTree = CommandTree(None)
#cmdTree.execute_command("*;1;off")
print "Command tree set; listening on ",MCAST_GRP,":",MCAST_PORT

while True:
    try:
        cmdTree.resetState()
        command = sock.recv(10240)
        cmd_parts = command.split(';')
        conditions = [room == cmd_parts[1] or cmd_parts[1] == "*", floor == cmd_parts[0] or cmd_parts[0] == "*"]
        if reduce(lambda x,y: x and y, conditions):
            print "cmd regards me, taking actions"
            cmdTree.execute_command(";".join(cmd_parts[2:]))
    except socket.timeout:
        #print "woke up"
        pass
