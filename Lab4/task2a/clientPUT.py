'''
Created on 08-09-2012

@author: Maciej Wasilak
'''
import serial
import sys

import thread
from twisted.internet.defer import Deferred
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.python import log

import txthings.coap as coap
import txthings.resource as resource


class Agent():
    """
    Example class which performs single PUT request to iot.eclipse.org
    port 5683 (official IANA assigned CoAP port), URI "/large-update".
    Request is sent 1 second after initialization.

    Payload is bigger than 64 bytes, and with default settings it
    should be sent as several blocks.
    """

    def __init__(self, protocol):
        self.protocol = protocol
        reactor.callLater(1, self.putResource)

    def putResource(self, payload = "0"):
        request = coap.Message(code=coap.PUT, payload=payload)
        request.opt.uri_path = ("led",)
        request.opt.content_format = coap.media_types_rev['text/plain']
        request.remote = ('192.168.17.86', coap.COAP_PORT)
        d = protocol.request(request)
        d.addCallback(self.printResponse)

    def printResponse(self, response):
        print 'Response Code: ' + coap.responses[response.code]
        print 'Payload: ' + response.payload

log.startLogging(sys.stdout)

endpoint = resource.Endpoint(None)
protocol = coap.Coap(endpoint)
client = Agent(protocol)

def thread_func(obj):
    ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)

    print "Subscribing button1"
    ser.write(chr(0b10011000))
    while True:
        try:
            cc = ser.read(1)
            if len(cc) < 1:
                continue
            cmd = ord(cc)
            #print cmd
            if cmd & 0b11111111 == 0b11000011:
                print "setting state of button on 1"
                obj.putResource("1")
            elif cmd & 0b11111111 == 0b11000010:
                print "setting state of button on 0"
                obj.putResource("0")
        except Exception:
            print "sth went wron with reading"

print "working"
thread.start_new_thread(thread_func, (client,))

reactor.listenUDP(61616, protocol)
reactor.run()
