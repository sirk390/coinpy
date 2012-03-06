# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from coinpy.tools.reactor.reactor import Reactor
from coinpy.lib.database.blockchain.db_blockchain import BSDDbBlockChainDatabase
from coinpy.model.genesis import GENESIS
from coinpy.lib.bitcoin.blockchain.blockchain import Blockchain
from coinpy.lib.bitcoin.blockchain_with_pools import BlockchainWithPools
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
from coinpy.node.bitcoinnode import BitcoinNode
from coinpy.node.network.bitcoin_port import BITCOIN_PORT
from coinpy.node.network.sockaddr import SockAddr
from coinpy.lib.database.bsddb_env import BSDDBEnv
import os
from coinpy.node.addrpool import AddrPool
from coinpy.node.addrpool_filler import AddrPoolFiller
from coinpy.node.peer_reconnector import PeerReconnector
from coinpy.node.transaction_publisher import TransactionPublisher
from coinpy_client.gui.model.wallet_set import WalletSet



class BitcoinClient():
    def __init__(self, log, nodeparams, data_directory): 
        self.nodeparams = nodeparams
        self.log = log
        self.dbenv_handles = {}
        self.dbenv = self.get_dbenv_handle(data_directory)
        # Reactor
        self.reactor = Reactor()
        # Blockchain
        self.database = BSDDbBlockChainDatabase(self.log, self.dbenv, self.nodeparams.runmode, data_directory)
        self.database.open_or_create(GENESIS[self.nodeparams.runmode])
        self.blockchain = Blockchain(self.log, self.database)
        # Pools
        self.blockchain_with_pools = BlockchainWithPools(self.blockchain, self.log)
        # Node
        self.node = BitcoinNode(self.reactor, self.blockchain_with_pools, self.nodeparams, self.log)
        
        # TMP: Add seed
        self.node.addr_pool.addpeer(SockAddr("127.0.0.1", BITCOIN_PORT[self.nodeparams.runmode]))
        
        # Wallets
        self.wallet_set = WalletSet(self.blockchain, self.nodeparams.runmode)
        self.transaction_publisher = TransactionPublisher(self.wallet_set, self.node, self.reactor)
        # Transaction
        #self.transaction_creator = TransactionCreator(self.nodeparams.runmode, self.blockchain)
        
    def get_dbenv_handle(self, directory):
        normdir = os.path.normcase(os.path.normpath(os.path.abspath(directory)))
        if normdir not in self.dbenv_handles:
            self.dbenv_handles[normdir] = BSDDBEnv(normdir)
        return self.dbenv_handles[normdir]
    
    def open_wallet(self, filename):
        directory, basename = os.path.split(filename)
        dbenv = self.get_dbenv_handle(directory)
        self.wallet_set.open_wallet(dbenv, basename)
   
    def start(self):
        self.reactor.start()

    def stop(self, callback):
        self.reactor.stop(callback)
 