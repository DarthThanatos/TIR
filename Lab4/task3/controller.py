'''
Created on 08-09-2012

@author: Maciej Wasilak
'''
import serial
import sys

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
        reactor.callLater(1, self.requestResource)

    def putRequest(self, payload = "0"):
        request = coap.Message(code=coap.PUT, payload=payload)
        request.opt.uri_path = ("led",)
        request.opt.content_format = coap.media_types_rev['text/plain']
        request.remote = ('192.168.200.128', coap.COAP_PORT)
        d = protocol.request(request)
        d.addCallback(self.printResponse)

    def requestResource(self):
        request = coap.Message(code=coap.GET)
        #Send request to "coap://iot.eclipse.org:5683/obs"
        request.opt.uri_path = ('button',)
        request.opt.observe = 1
        request.remote = ("192.168.200.128", coap.COAP_PORT)
        d = protocol.request(request, observeCallback=self.printLaterResponse)
        d.addCallback(self.printResponse)
        d.addErrback(self.noResponse)

    def printLaterResponse(self, response):
        print 'Observe result: ' + response.payload
        try:
            value = int(response.payload)
            if value == 1:
                self.putRequest("1")
            elif value == 0:
                self.putRequest("0")
        except:
            print "Error"

    def printResponse(self, response):
        print 'Response Code: ' + coap.responses[response.code]
        print 'Payload: ' + response.payload

    def noResponse(self, failure):
        print 'Failed to fetch resource:'
        print failure
        #reactor.stop()

log.startLogging(sys.stdout)

endpoint = resource.Endpoint(None)
protocol = coap.Coap(endpoint)
client = Agent(protocol)

reactor.listenUDP(61616, protocol)
reactor.run()
