# -*- coding:utf-8 -*-
"""
Created on 16 Apr 2012

@author: kris
"""
# no wallet dependency, but blockchain dependency
from coinpy.node.version_exchange_node import VersionExchangeService
from coinpy.node.logic.blockchain_downloader import BlockchainDownloader
from coinpy.node.logic.blockchain_server import BlockchainServer
from coinpy.node.peer_reconnector import PeerReconnector
from coinpy.node.addrpool_filler import AddrPoolFiller
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
from coinpy.node.addrpool import AddrPool
from coinpy.node.basic_node import BasicNode

class BitcoinNode(BasicNode):
    def __init__(self, reactor, blockchain_with_pools, params, log):
        super(BitcoinNode, self).__init__(reactor, lambda : 0, params, log)
        
        self.blockchain_with_pools = blockchain_with_pools
        self.add_service(BlockchainDownloader(reactor, blockchain_with_pools, self, self.log))
        self.add_service(BlockchainServer(reactor, self, blockchain_with_pools, log))
