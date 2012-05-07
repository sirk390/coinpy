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
    def __init__(self, blockchain, txpool, params, log, findpeers=True):
        super(BitcoinNode, self).__init__(lambda : 0, params, log, findpeers)
        self.blockchain = blockchain
        self.txpool = txpool
        self.blockserver = BlockchainServer(self, blockchain, self.txpool, log)
        self.blockdl = BlockchainDownloader(blockchain, self, self.log)
        self.txdl = TxDownloadService(self, blockchain, self.txpool, log)
        self.add_service(self.blockserver)
        self.add_service(self.blockdl)
        self.add_service(self.txdl)
