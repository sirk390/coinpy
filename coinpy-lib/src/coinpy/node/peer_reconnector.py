# -*- coding:utf-8 -*-
"""
Created on 26 Feb 2012

@author: kris
"""
import random

class PeerReconnector():
    def __init__(self, addrpool, node, min_connections=4):
        self.addrpool = addrpool
        self.node = node
        self.min_connections = min_connections
        
        self.node.subscribe(self.node.EVT_CONNECTED, self.on_peer_connected)
        self.node.subscribe(self.node.EVT_DISCONNECTED, self.on_peer_disconnected)
        self.addrpool.subscribe(self.addrpool.EVT_ADDED_ADDR, self.on_added_addr)
        self.check_connection_count()
        
        self.connecting_peers = set()

    def on_peer_connected(self, event):
        self.addrpool.connected(event.handler.sockaddr)
        self.connecting_peers.remove(event.handler.sockaddr)
        
    def on_peer_disconnected(self, event):
        addr = event.handler.sockaddr
        if addr in self.connecting_peers:
            self.addrpool.failed(addr)
            self.connecting_peers.remove(addr)
        else:
            self.addrpool.disconnected(addr)
        self.check_connection_count()
            
    def check_connection_count(self):
        missing_count = int(self.min_connections - \
                        len(self.node.connection_manager.connected_peers) \
                        - (len(self.node.connection_manager.connecting_peers) / 5.0))
                        
        #print "check_connection_count", missing_count
        if missing_count > 0:
            peeraddrs = self.addrpool.getpeers(missing_count)
            for peeraddr in peeraddrs:
                self.node.connect_peer(peeraddr)
                self.connecting_peers.add(peeraddr)
                
    def on_added_addr(self, event):
        self.check_connection_count()
        
        