# -*- coding:utf-8 -*-
"""
Created on 26 Feb 2012

@author: kris
"""
import random
from coinpy.model.protocol.messages.getaddr import msg_getaddr
from coinpy.model.protocol.messages.types import MSG_ADDR
from coinpy.node.node import Node
from coinpy.node.network.sockaddr import SockAddr

"""
AddrPoolFiller:
    This objects listens to a node and fills an 'addr_pool' passed as a parameter
    until it contains 'min_addrpool_size' addresses using:
        get_addr() messages if some peers are connected
        bootstrapping if no peers are connected
"""
class AddrPoolFiller():
    def __init__(self, bootstrapper, node, addr_pool, min_addrpool_size=10):
        self.bootstrapper = bootstrapper
        self.node = node
        self.addr_pool = addr_pool
        self.min_addrpool_size = min_addrpool_size
        self.bootstrapper.subscribe(self.bootstrapper.EVT_FOUND_PEER, self.on_bootstrapped_peer)
        self.node.subscribe((Node.EVT_MESSAGE, MSG_ADDR), self.on_addr)
        self.node.subscribe(Node.EVT_CONNECTED, self.on_connected)
        self.node.subscribe(Node.EVT_DISCONNECTED, self.on_disconnected)
        self.check_addrpool()
        
    def check_addrpool(self):
        if len(self.addr_pool.known_peers) < self.min_addrpool_size:
            if len(self.node.connection_manager.connected_peers):
                #take a random connected peer and request more peer addresses
                peer = random.sample(self.node.connection_manager.connected_peers, 1)[0]
            else:
                #bootstrap
                self.bootstrapper.bootstrap()
    
    #might require a get_addr()
    def on_connected(self, event):
        self.check_addrpool()
        
    #might require a bootstrap
    def on_disconnected(self, event):
        self.check_addrpool()
        
    def on_addr(self, event):
        for timenetaddr in event.message.timenetaddr_list:
            peeraddr = SockAddr(timenetaddr.netaddr.ip, timenetaddr.netaddr.port)
            self.addr_pool.addpeer(peeraddr)
                    
    def on_bootstrapped_peer(self, event):
        self.addr_pool.addpeer(event.peeraddress)
            
            