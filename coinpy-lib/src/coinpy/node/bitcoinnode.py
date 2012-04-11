# -*- coding:utf-8 -*-
"""
Created on 17 Sep 2011

@author: kris
"""
from coinpy.node.node import Node
from coinpy.node.logic.blockchain_server import BlockchainServer
from coinpy.node.logic.blockchain_downloader import BlockchainDownloader
from coinpy.model.protocol.messages.types import MESSAGE_TYPES
from coinpy.node.version_exchange_node import VersionExchangeNode
from coinpy.node.trickler import Trickler
from coinpy.node.addrpool import AddrPool
from coinpy.node.addrpool_filler import AddrPoolFiller
from coinpy.node.peer_reconnector import PeerReconnector
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper

# no wallet dependency
class BitcoinNode(VersionExchangeNode):
    def __init__(self, reactor, blockchain_with_pools, params, log):
        super(BitcoinNode, self).__init__(reactor, lambda : 0, params, log)
        #bootstraper
        self.blockchain_with_pools = blockchain_with_pools
        self.bootstrapper = Bootstrapper(reactor, params.runmode, self.log)
        self.addr_pool = AddrPool(reactor)
        AddrPoolFiller(self.bootstrapper, self, self.addr_pool)
        PeerReconnector(self.addr_pool, self, min_connections=params.targetpeers)
        BlockchainDownloader(reactor, blockchain_with_pools, self, self.log)
        BlockchainServer(reactor, self, blockchain_with_pools, log)
        self.trickler = Trickler(reactor, self)
