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
from coinpy.node.addrpool_filler import AddPoolFiller
from coinpy.node.peer_reconnector import PeerReconnector

class CoinpyService():
    def __init__(self, log, nodeparams, data_directory): 
        self.nodeparams = nodeparams
        self.log = log
        self.reactor = Reactor()
        self.dbenv_handles = {}
        self.dbenv = self.get_dbenv_handle(data_directory)
        #blockchain database
        self.database = BSDDbBlockChainDatabase(self.log, self.dbenv, self.nodeparams.runmode, data_directory)
        self.database.open_or_create(GENESIS[self.nodeparams.runmode])
        self.blockchain = Blockchain(self.log, self.database)
        self.blockchain_with_pools = BlockchainWithPools(self.blockchain, self.log)
        #bootstraper
        self.bootstrapper = Bootstrapper(self.nodeparams.runmode, self.log)
        #node
        self.node = BitcoinNode(self.reactor, self.blockchain_with_pools, self.nodeparams, self.log)
        self.addr_pool = AddrPool()
        self.addr_pool_filler = AddPoolFiller(self.bootstrapper, self.node, self.addr_pool)
        self.peer_reconnector = PeerReconnector(self.addr_pool, self.node, min_connections=4)
        #self.node.add_peer_address(SockAddr("127.0.0.1", BITCOIN_PORT[self.nodeparams.runmode]))
        
        self.addr_pool.addpeer(SockAddr("127.0.0.1", BITCOIN_PORT[self.nodeparams.runmode]))
        #TMP: Add seed peer
        #self.node.add_peer_address(SockAddr("127.0.0.1", BITCOIN_PORT[self.nodeparams.runmode]))

    def get_dbenv_handle(self, directory):
        normdir = os.path.normcase(os.path.normpath(os.path.abspath(directory)))
        if normdir not in self.dbenv_handles:
            self.dbenv_handles[normdir] = BSDDBEnv(normdir)
        return self.dbenv_handles[normdir]
           
   
    def start(self):
        self.reactor.start()

    def stop(self, callback):
        self.reactor.stop(callback)
 
