# -*- coding:utf-8 -*-
"""
Created on 17 Sep 2011

@author: kris
"""
from coinpy.node.node import Node
from coinpy.node.logic.version_exchange import VersionExchangeService

"""BasicNode: bootstrap, maintain basic peer network connections. 

Handles the following tasks:
    - reconnect to "targetpeers" peers, handle version/verack exchange.
    - fill an address pool using bootstrap and "getaddr" messages.
    - keep a list of banned peers.
"""
class BasicNode(Node):
    def __init__(self, get_blockchain_height, params, log):
        super(BasicNode, self).__init__(params, log)
        
        self.version_service = VersionExchangeService(self, get_blockchain_height, params, log)
        
    def emit_message(self, eventtype, **args): 
        self.fire(eventtype, **args)
                    
    def misbehaving(self, handler, reason):
        self.log.warning("peer misbehaving: %s" % reason)
        #self.addr_pool.misbehaving(handler.sockaddr, reason)
        #self.connection_manager.disconnect_peer(handler.sockaddr)

