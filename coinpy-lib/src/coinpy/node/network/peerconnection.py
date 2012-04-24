# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from coinpy.node.network.peerhandler import PeerHandler
from coinpy.lib.serialization.exceptions import MissingDataException
from coinpy.tools.observer import Observable
from coinpy.tools.reactor.reactor import reactor

class PeerConnection(PeerHandler):
    EVT_NEW_MESSAGE = Observable.createevent()
    #TODO: merge with PeerHandler?
    def __init__(self, sockaddr, msg_serializer, sock, log):
        PeerHandler.__init__(self, sockaddr, sock)
        #self.subscribe(self.EVT_CONNECT, self.on_connect)
        self.msg_serializer = msg_serializer
        self.incommingbuffer = ""
        self.log = log

    def readable(self):
        return (True)
        
    def handle_read(self):
        self.incommingbuffer += self.recv(8192*10)
        self._process_incomming_buffer()
    
    def clear_incomming_buffers(self):
        self.incommingbuffer = []
        
    def _process_incomming_buffer(self):
        cursor = 0
        #while cursor < len(self.incommingbuffer):
        try:
            msg, cursor = self.msg_serializer.deserialize(self.incommingbuffer, cursor)
        except MissingDataException:
            #print traceback.format_exc()
            #self.log.warning("Read Incomplete")
            #print "cursor = %d:%s" % (cursor, traceback.format_exc())
            return
        self.incommingbuffer = self.incommingbuffer[cursor:]
        self.fire(self.EVT_NEW_MESSAGE, handler=self, message=msg)
        #self.on_message(msg)
        #call again for the rest of the message
        reactor.call(self._process_incomming_buffer)
        
    def send_message(self, message):
        self.send(self.msg_serializer.serialize(message))
        
"""      
    def on_message(self, msg):
        print "received message: ", msg
        if (msg.type == MSG_VERSION):
            verack = self.msg_encoder.encode(msg_verack())
            #print hexdump(verack)
            self.send(verack )
            self.send_version()
"""
# def send_version(self):
"""vermsg = msg_version(version = self.coinpy.node.params.version, 
                     services=self.coinpy.node.params.enabledservices, 
                     timestamp=time.time(), 
                     addr_me=self.coinpy.node.addr_me, 
                     addr_you=self.addr_you, 
                     nonce=self.coinpy.node.params.nonce, 
                     sub_version_num=self.coinpy.node.params.sub_version_num,
                     start_height=100)"""
#print "sending version to", self.sockaddr, vermsg 
#print hexdump(verack)
    

#self.send(self.msg_encoder.encode(vermsg))
#print hexdump(data)

        