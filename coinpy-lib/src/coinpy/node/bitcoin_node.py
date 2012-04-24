# -*- coding:utf-8 -*-
"""
Created on 16 Apr 2012

@author: kris
"""
from coinpy.node.logic.blockchain_downloader import BlockchainDownloader
from coinpy.node.logic.blockchain_server import BlockchainServer
from coinpy.node.basic_node import BasicNode

"""BitcoinNode: Classic heavy weight Bitcoin Node.

Support of:
    - blockchain downloading
    - blockchain uploading
The class depends on the blockchain, but not on the wallet. 
"""
class BitcoinNode(BasicNode):
    def __init__(self, blockchain_with_pools, params, log):
        super(BitcoinNode, self).__init__(lambda : 0, params, log)
        
        self.blockchain_with_pools = blockchain_with_pools
        self.add_service(BlockchainDownloader(blockchain_with_pools, self, self.log))
        self.add_service(BlockchainServer(self, blockchain_with_pools, log))
