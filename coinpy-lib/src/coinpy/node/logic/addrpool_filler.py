# -*- coding:utf-8 -*-
"""
Created on 26 Feb 2012

@author: kris
"""
import random
from coinpy.model.protocol.messages.getaddr import GetaddrMessage
from coinpy.model.protocol.messages.types import MSG_ADDR
from coinpy.node.node import Node
from coinpy.node.network.sockaddr import SockAddr
from coinpy.node.logic.version_exchange import VersionExchangeService
from coinpy.tools.reactor.reactor import reactor

"""Fill 'addr_pool' by bootstrapping and sending get_addr() messages.
 
AddrPoolFiller fills 'addr_pool' until it contains 'min_addrpool_size' addresses using:
        get_addr() messages if some peers are connected
        bootstrapping if no peers are connected
"""
class AddrPoolFiller():
    def __init__(self, node, bootstrapper, addr_pool, min_addrpool_size=10):
        self.bootstrapper = bootstrapper
        self.addr_pool = addr_pool
        self.min_addrpool_size = min_addrpool_size
        self.bootstrapper.subscribe(self.bootstrapper.EVT_FOUND_PEER, self.on_bootstrapped_peer)
    
        self.node = node
        self.node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_ADDR), self.on_addr)
        self.node.subscribe(VersionExchangeService.EVT_VERSION_EXCHANGED, self.on_version_exchanged)
        self.node.subscribe(Node.EVT_DISCONNECTED, self.on_disconnected)
        
        reactor.call(self.check_addrpool)
        
    def check_addrpool(self):
        if len(self.addr_pool.known_peers) < self.min_addrpool_size:
            if self.node.connected_peer_count():
                #take a random connected peer and request more peer addresses
                peer = random.sample(self.node.peers_with_state(Node.PEER_CONNECTED), 1)[0]
                self.node.send_message(peer, GetaddrMessage())
            else:
                #bootstrap
                self.bootstrapper.bootstrap()
    
    #might require a get_addr()
    def on_version_exchanged(self, event):
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
            
            