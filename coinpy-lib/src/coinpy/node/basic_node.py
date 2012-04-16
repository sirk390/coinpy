# -*- coding:utf-8 -*-
"""
Created on 17 Sep 2011

@author: kris
"""
from coinpy.node.node import Node
from coinpy.node.logic.blockchain_server import BlockchainServer
from coinpy.node.logic.blockchain_downloader import BlockchainDownloader
from coinpy.model.protocol.messages.types import MESSAGE_TYPES
from coinpy.node.trickler import Trickler
from coinpy.node.addrpool import AddrPool
from coinpy.node.addrpool_filler import AddrPoolFiller
from coinpy.node.peer_reconnector import PeerReconnector
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
from coinpy.node.version_exchange_node import VersionExchangeService

# no wallet dependency, but blockchain dependency
class BasicNode(Node):
    def __init__(self, reactor, get_blockchain_height, params, log):
        super(BasicNode, self).__init__(reactor, params, log)
        self.addr_pool = AddrPool(reactor)
        self.bootstrapper = Bootstrapper(reactor, params.runmode, self.log)
        
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

