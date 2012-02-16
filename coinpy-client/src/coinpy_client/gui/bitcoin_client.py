# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from coinpy.tools.reactor.reactor import Reactor
from coinpy.lib.database.bsddb_env import BSDDBEnv
from coinpy.model.genesis import GENESIS
from coinpy.lib.database.blockchain.db_blockchain import BSDDbBlockChainDatabase
from coinpy.lib.bitcoin.blockchain.blockchain import Blockchain
from coinpy.lib.bitcoin.blockchain_with_pools import BlockchainWithPools
from coinpy.lib.bitcoin.wallet.wallet import Wallet
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
from coinpy.node.bitcoinnode import BitcoinNode
import threading
import os
from coinpy.tools.observer import Observable
from coinpy.node.network.sockaddr import SockAddr
from coinpy.node.network.bitcoin_port import BITCOIN_PORT
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase

class BitcoinClient(Observable):
    EVT_WALLET_OPENED = Observable.createevent()
    
    def __init__(self, logger, nodeparams, data_directory): 
        Observable.__init__(self)
        self.log = logger
        #wallets
        self.wallets = []           # id => Wallet
        self.wallet_filenames = {}  # id => Wallet
        self.dbenv_handles = {}     # directory => DBEnv
        
        self.nodeparams = nodeparams
        self.reactor = Reactor()
        #blockchain database
        self.database = BSDDbBlockChainDatabase(self.log, self.get_dbenv_handle(data_directory), self.nodeparams.runmode, data_directory)
        self.database.open_or_create(GENESIS[self.nodeparams.runmode])
        self.blockchain = Blockchain(self.log, self.database)
        self.blockchain_with_pools = BlockchainWithPools(self.blockchain, self.log)
        #bootstraper
        self.bootstrapper = Bootstrapper(self.nodeparams.runmode, self.log)
        #node
        self.node = BitcoinNode(self.reactor, self.blockchain_with_pools, self.nodeparams, self.log)
        self.bootstrapper.subscribe(Bootstrapper.EVT_FOUND_PEER, self.on_found_peer)
        self.node.subscribe(BitcoinNode.EVT_NEED_BOOTSTRAP, self.on_need_peers)

       
    def get_dbenv_handle(self, directory):
        normdir = os.path.normcase(os.path.normpath(os.path.abspath(directory)))
        if normdir not in self.dbenv_handles:
            self.dbenv_handles[normdir] = BSDDBEnv(normdir)
        return self.dbenv_handles[normdir]
    
    def open_wallet(self, filename):
        directory, basename = os.path.split(filename)
        wallet_db = BSDDBWalletDatabase(self.get_dbenv_handle(directory), filename)
        wallet = Wallet(wallet_db)
        self.wallets.append(wallet)
        self.wallet_filenames[wallet] = filename
        self.fire(self.EVT_WALLET_OPENED, wallet=wallet, filename=filename)
        
    def on_found_peer(self, event):
        self.log.info("Found peers: %s" % (str(event.peeraddress)))
        self.node.add_peer_address(event.peeraddress)
        
    def on_need_peers(self, event):
        self.log.info("Bootstraping...")
        self.node.add_peer_address(SockAddr("127.0.0.1", BITCOIN_PORT[self.nodeparams.runmode]))
        #self.bootstrapper.bootstrap()

    def start(self):
        self.reactor.start()

    def stop(self):
        self.reactor.stop()
        