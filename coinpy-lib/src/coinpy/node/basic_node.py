# -*- coding:utf-8 -*-
"""
Created on 17 Sep 2011

@author: kris
"""
from coinpy.node.node import Node
from coinpy.node.addrpool import AddrPool
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
from coinpy.node.logic.peer_reconnector import PeerReconnector
from coinpy.node.logic.version_exchange import VersionExchangeService
from coinpy.node.logic.addrpool_filler import AddrPoolFiller

"""BasicNode: bootstrap, maintain basic peer network connections. 

Handles the following tasks:
    - reconnect to "targetpeers" peers, handle version/verack exchange.
    - fill an address pool using bootstrap and "getaddr" messages.
    - keep a list of banned peers.
"""
class BasicNode(Node):
    def __init__(self, get_blockchain_height, params, log):
        super(BasicNode, self).__init__(params, log)
        self.addr_pool = AddrPool()
        self.bootstrapper = Bootstrapper(params.runmode, self.log)
        
        self.add_service(PeerReconnector(self.addr_pool, min_connections=params.targetpeers))
        self.version_service = VersionExchangeService(get_blockchain_height, params, log)
        self.add_service(self.version_service)
        self.add_service(AddrPoolFiller(self.bootstrapper, self.addr_pool))
        
    def emit_message(self, eventtype, **args): 
        self.fire(eventtype, **args)
        
    def add_service(self, service): 
        service.install(self)
            
    def misbehaving(self, handler, reason):
        self.log.warning("peer misbehaving: %s" % reason)
        self.addr_pool.misbehaving(handler.sockaddr, reason)
        self.connection_manager.disconnect_peer(handler.sockaddr)

