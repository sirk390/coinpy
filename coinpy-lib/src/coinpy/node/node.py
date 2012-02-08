# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from coinpy.model.protocol.services import SERVICES_NONE, SERVICES_NODE_NETWORK
from coinpy.node.network.connection_manager import ConnectionManager
from coinpy.model.protocol.structures.netaddr import netaddr
from coinpy.node.network.peerconnectionfactory import PeerConnectionFactory
from coinpy.node.network.peerconnection import PeerConnection
from coinpy.model.protocol.messages.types import MSG_VERSION, MSG_INV, MSG_TX, MSG_BLOCK,\
    MSG_VERACK, MESSAGE_TYPES
from coinpy.model.protocol.messages.verack import msg_verack
from coinpy.model.protocol.messages.version import msg_version
import time
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.invitem import INV_TX, INV_BLOCK
from coinpy.model.protocol.messages.getdata import msg_getdata
from coinpy.node.network.sockaddr import SockAddr
from coinpy.lib.serialization.messages.s11n_message import MessageSerializer

"""
    Bitcoin node that uses the standard binary protocol.
    https://en.bitcoin.it/wiki/Protocol_specification
"""
class Node(Observable):
    EVT_NEED_BOOTSTRAP = Observable.createevent()
    EVT_MESSAGE = Observable.createevent()
    EVT_CONNECTED = Observable.createevent()
    EVT_DISCONNECTED = Observable.createevent()
            
    def __init__(self, reactor, params, log):
        super(Node, self).__init__()
        self.reactor = reactor
        self.params = params
        self.log = log
        self.addr_me = netaddr(self.params.enabledservices, "192.168.1.1", 78)
        
        self.message_encoder = MessageSerializer(self.params.runmode, log)
        self.connection_factory = PeerConnectionFactory(self.message_encoder, log)
        self.connection_manager = ConnectionManager(reactor, SockAddr('localhost', self.params.port), self.connection_factory, log)
        self.connection_manager.subscribe(ConnectionManager.EVT_CONNECTED_HANDLER, self.__on_connected)
        self.connection_manager.subscribe(ConnectionManager.EVT_DISCONNECTED_HANDLER, self.__on_disconnected)
        self.reactor.schedule_each(1, self.check_bootstrap)

    def __on_connected(self, event):
        event.handler.subscribe(PeerConnection.EVT_NEW_MESSAGE, self.__on_message)
        self.on_connected(event)
        
    def __on_disconnected(self, event):
        self.on_disconnected(event)
        
    def __on_message(self, event):
        #self.log.info("Message from %s : %s" % (event.handler, event.message))
        self.on_message(event)

    """ --- redefined in subclasses to filter messages """
    def on_connected(self, event):
        self.fire(self.EVT_CONNECTED, handler=event.handler)
    
    def on_message(self, event):
        self.fire_message_event(event.handler, event.message)
        
    def on_disconnected(self, event):
        self.fire(self.EVT_DISCONNECTED, handler=event.handler)

    """ --- """
    def fire_message_event(self, handler, message):
        self.fire(self.EVT_MESSAGE, message=message, handler=handler)
      
    def check_bootstrap(self):
        if len(self.connection_manager.known_peer_addresses) == 0:
            self.fire(self.EVT_NEED_BOOTSTRAP)
        #self.connection_manager.loop_iteration()
        
    def remove_peer(self, addr):
        self.connection_manager.remove_peer(addr)
        
    def add_peer_address(self, address):
        self.connection_manager.add_peer_address(address)
          
    def send_message(self, peer, message):
        peer.send_message(message)
         
    def misbehaving(self, peer, reason):
        self.log.warning("peer misbehaving: %s" % reason)
        self.remove_peer(peer.sockaddr)
    