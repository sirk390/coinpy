# -*- coding:utf-8 -*-
"""
Created on 26 Feb 2012

@author: kris
"""

class PeerReconnector():
    def __init__(self, addrpool, min_connections=4):
        self.addrpool = addrpool
        self.min_connections = min_connections
        self.connecting_peers = set()
        
    def install(self, node):
        self.node = node
        self.node.subscribe(self.node.EVT_CONNECTED, self.on_peer_connected)
        self.node.subscribe(self.node.EVT_DISCONNECTED, self.on_peer_disconnected)
        self.addrpool.subscribe(self.addrpool.EVT_ADDED_ADDR, self.on_added_addr)
        self.check_connection_count()
           
    def on_peer_connected(self, event):
        self.addrpool.connected(event.handler.sockaddr)
        self.connecting_peers.remove(event.handler.sockaddr)
        
    def on_peer_disconnected(self, event):
        addr = event.handler.sockaddr
        if addr in self.connecting_peers:
            self.addrpool.failed(addr)
        self.check_connection_count()
            
    def check_connection_count(self):
        missing_count = int(self.min_connections - \
                        len(self.node.connection_manager.connected_peers) \
                        - (len(self.node.connection_manager.connecting_peers) / 2.0))
                        
        if missing_count > 0:
            connected_or_connecting = set(self.node.connection_manager.peers)
            peeraddrs = self.addrpool.getpeers(missing_count, exclude=connected_or_connecting)
            for peeraddr in peeraddrs:
                self.node.connect_peer(peeraddr)
                self.connecting_peers.add(peeraddr)
                
    def on_added_addr(self, event):
        self.check_connection_count()
        
        