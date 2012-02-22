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

class CoinpyService():
    def __init__(self, log, nodeparams, dbenv, data_directory): 
        self.nodeparams = nodeparams
        self.log = log
        self.reactor = Reactor()
        #blockchain database
        self.database = BSDDbBlockChainDatabase(self.log, dbenv, self.nodeparams.runmode, data_directory)
        self.database.open_or_create(GENESIS[self.nodeparams.runmode])
        self.blockchain = Blockchain(self.log, self.database)
        self.blockchain_with_pools = BlockchainWithPools(self.blockchain, self.log)
        #bootstraper
        self.bootstrapper = Bootstrapper(self.nodeparams.runmode, self.log)
        #node
        self.node = BitcoinNode(self.reactor, self.blockchain_with_pools, self.nodeparams, self.log)
        self.bootstrapper.subscribe(Bootstrapper.EVT_FOUND_PEER, self.on_found_peer)
        self.node.subscribe(BitcoinNode.EVT_NEED_BOOTSTRAP, self.on_need_peers)
        #TMP: Add seed peer
        self.node.add_peer_address(SockAddr("127.0.0.1", BITCOIN_PORT[self.nodeparams.runmode]))
            
    def on_found_peer(self, event):
        #self.log.info("Found peers: %s" % (str(event.peeraddress)))
        self.node.add_peer_address(event.peeraddress)
        
    def on_need_peers(self, event):
        self.log.info("Bootstraping...")
        self.bootstrapper.bootstrap()

    def start(self):
        self.reactor.start()

    def stop(self, callback):
        self.reactor.stop(callback)
 
