# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from coinpy.node.network.connection_manager import ConnectionManager
from coinpy.node.network.peerconnectionfactory import PeerConnectionFactory
from coinpy.node.network.peerconnection import PeerConnection
from coinpy.tools.observer import Observable
from coinpy.node.network.sockaddr import SockAddr
from coinpy.lib.serialization.messages.s11n_message import MessageSerializer

"""Node: connect, disconnect peers, send and receive bitcoin messages. 

No logic included.
"""
class Node(Observable):
    EVT_NEED_PEERS = Observable.createevent()
    EVT_BASIC_MESSAGE = Observable.createevent()
    EVT_CONNECTING = Observable.createevent()
    EVT_CONNECTED = Observable.createevent()
    EVT_DISCONNECTED = Observable.createevent()
            
    def __init__(self, reactor, params, log, min_connection_count=5):
        super(Node, self).__init__(reactor)
        self.min_connection_count = min_connection_count
        self.reactor = reactor
        self.params = params
        self.log = log
        
        self.message_encoder = MessageSerializer(self.params.runmode, log)
        self.connection_factory = PeerConnectionFactory(self.reactor, self.message_encoder, log)
        self.connection_manager = ConnectionManager(reactor, SockAddr('localhost', self.params.port), self.connection_factory, log)
        self.connection_manager.subscribe(ConnectionManager.EVT_CONNECTED_PEER, self.__on_connected)
        self.connection_manager.subscribe(ConnectionManager.EVT_CONNECTING_PEER, self.__on_connecting)
        self.connection_manager.subscribe(ConnectionManager.EVT_DISCONNECTED_PEER, self.__on_disconnected)

    def __on_connected(self, event):
        event.handler.subscribe(PeerConnection.EVT_NEW_MESSAGE, self.__on_message)
        self.fire(self.EVT_CONNECTED, handler=event.handler)
        
    def __on_connecting(self, event):
        self.fire(self.EVT_CONNECTING, handler=event.handler)
        
    def __on_disconnected(self, event):
        self.fire(self.EVT_DISCONNECTED, handler=event.handler)
        
    def __on_message(self, event):
        handler, message = event.handler, event.message
        self.fire(self.EVT_BASIC_MESSAGE, message=message, handler=handler)
      
    def connect_peer(self, addr):
        self.connection_manager.connect_peer(addr)
          
    def send_message(self, peer, message):
        peer.send_message(message)

