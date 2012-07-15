# -*- coding:utf-8 -*-
"""
Created on 16 Apr 2012

@author: kris
"""
from coinpy.node.logic.blockchain_downloader import BlockchainDownloader
from coinpy.node.logic.blockchain_server import BlockchainServer
from coinpy.node.basic_node import BasicNode
from coinpy.lib.bitcoin.pools.transactionpool import TransactionPool
from coinpy.node.logic.txdownloadservice import TxDownloadService

"""BitcoinNode: Classic heavy weight Bitcoin Node.

Support of:
    - blockchain downloading
    - blockchain uploading
The class depends on the blockchain, but not on the wallet. 
"""
class BitcoinNode(BasicNode):
    def __init__(self, blockchain, txpool, process_pool, params, log):
        super(BitcoinNode, self).__init__(blockchain.get_height, params, log)
        self.blockchain = blockchain
        self.txpool = txpool
        self.blockserver = BlockchainServer(self, blockchain, self.txpool, log)
        self.blockdl = BlockchainDownloader(self, blockchain, process_pool, self.log)
        self.txdl = TxDownloadService(self, blockchain, self.txpool, process_pool, log)

