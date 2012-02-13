# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from coinpy.node.network.reactor import Reactor
from coinpy.lib.database.bsddb_env import BsdDbEnv
from coinpy.model.genesis import GENESIS
from coinpy.lib.database.blockchain.db_blockchain import BSDDbBlockChainDatabase
from coinpy.lib.bitcoin.blockchain.blockchain import Blockchain
from coinpy.lib.bitcoin.blockchain_with_pools import BlockchainWithPools
from coinpy.lib.database.wallet.wallet_database import WalletDatabase
from coinpy.lib.bitcoin.wallet.wallet import Wallet
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
from coinpy.node.bitcoinnode import BitcoinNode
import threading

class BitcoinClient():
    def __init__(self, logger, nodeparams, data_directory): 
        self.log = logger
        self.nodeparams = nodeparams
        self.reactor = Reactor(self.log)
        #blockchain database
        self.bsddbenv = BsdDbEnv(directory=data_directory)
        self.database = BSDDbBlockChainDatabase(self.log, self.bsddbenv, self.nodeparams.runmode, data_directory)
        self.database.open_or_create(GENESIS[self.nodeparams.runmode])
        self.blockchain = Blockchain(self.log, self.database)
        self.blockchain_with_pools = BlockchainWithPools(self.blockchain, self.log)
        #wallet
        self.wallet = Wallet(WalletDatabase(data_directory, "wallet.dat"), self.blockchain)
        #bootstraper
        self.bootstrapper = Bootstrapper(self.nodeparams.runmode, self.log)
        #node
        self.node = BitcoinNode(self.reactor, self.blockchain_with_pools, self.nodeparams, self.log)
        self.bootstrapper.subscribe(Bootstrapper.EVT_FOUND_PEER, self.on_found_peer)
        self.node.subscribe(BitcoinNode.EVT_NEED_BOOTSTRAP, self.on_need_peers)
        #bitcoin thread

        
    def on_found_peer(self, event):
        self.log.info("Found peers: %s" % (str(event.peeraddress)))
        self.node.add_peer_address(event.peeraddress)
        
    def on_need_peers(self, event):
        self.log.info("Bootstraping...")
        self.bootstrapper.bootstrap()

    def start(self):
        self.reactor.start()

    def stop(self):
        self.reactor.stop()
        