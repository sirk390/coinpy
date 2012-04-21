# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from coinpy.lib.database.blockchain.db_blockchain import BSDDbBlockChainDatabase
from coinpy.model.genesis import GENESIS
from coinpy.lib.bitcoin.blockchain.blockchain import Blockchain
from coinpy.lib.bitcoin.blockchain_with_pools import BlockchainWithPools
from coinpy.node.network.bitcoin_port import BITCOIN_PORT
from coinpy.node.network.sockaddr import SockAddr
from coinpy.lib.database.bsddb_env import BSDDBEnv
import os
from coinpy.node.transaction_publisher import TransactionPublisher
from coinpy_client.model.account_set import AccountSet
from coinpy.lib.bitcoin.wallet.wallet import Wallet
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.lib.bitcoin.wallet.wallet_account import WalletAccount
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
import logging.handlers
from coinpy.tools.bsddb.bsddb_file_id import bsddb_read_file_uid
from coinpy.node.bitcoin_node import BitcoinNode



class BitcoinClient():
    def __init__(self, reactor, log, clientparams): 
        self.clientparams = clientparams
        self.log = log
        self.dbenv_handles = {} 
        self.account_infos = {} # account => (handle, dirname, filename)
        self.dbenv = self.get_dbenv_handle(clientparams.data_directory)
        self.reactor = reactor
        # Logfile
        handler = logging.handlers.RotatingFileHandler(os.path.join(clientparams.data_directory,clientparams.logfilename), maxBytes=1024*1024*8, backupCount=5)
        self.log.addHandler(handler)
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(fmt)
        # Blockchain
        self.database = BSDDbBlockChainDatabase(self.log, self.dbenv, clientparams.runmode)
        self.database.open_or_create(GENESIS[clientparams.runmode])
        self.blockchain = Blockchain(self.reactor, self.log, self.database)
        # Pools
        self.blockchain_with_pools = BlockchainWithPools(self.reactor, self.blockchain, self.log)
        # Node
        nodeparams = NodeParams(runmode=clientparams.runmode,
                                port=clientparams.port,
                                version=60000,
                                enabledservices=SERVICES_NODE_NETWORK,
                                nonce=clientparams.nonce,
                                sub_version_num=clientparams.sub_version_num,
                                targetpeers=clientparams.targetpeers)
        self.node = BitcoinNode(self.reactor, self.blockchain_with_pools, nodeparams, self.log)
        # TMP: Add seed
        self.node.addr_pool.addpeer(SockAddr("127.0.0.1", BITCOIN_PORT[clientparams.runmode]))
        # Wallets
        self.account_set = AccountSet(self.reactor)
        
        
    def get_dbenv_handle(self, directory):
        normdir = os.path.normcase(os.path.normpath(os.path.abspath(directory)))
        if normdir not in self.dbenv_handles:
            self.dbenv_handles[normdir] = BSDDBEnv(normdir)
        return self.dbenv_handles[normdir]
    
    def new_wallet(self, filename):
        directory, basename = os.path.split(filename)
        dbenv = self.get_dbenv_handle(directory)
        
        wallet_db = BSDDBWalletDatabase(dbenv, basename)
        wallet_db.create()
    
    def open_wallet(self, filename):
        directory, basename = os.path.split(filename)
        dbenv = self.get_dbenv_handle(directory)
        
        uid = bsddb_read_file_uid(filename)
        if uid in dbenv.open_file_uids:
            raise Exception("Multiple wallets with the same uid unsupported in the same directory.")
        dbenv.open_file_uids.add(uid)
        wallet_db = BSDDBWalletDatabase(dbenv, basename)
        wallet = Wallet(self.reactor, wallet_db, self.clientparams.runmode)
        account = WalletAccount(self.reactor, self.log, basename, wallet, self.blockchain)
        TransactionPublisher(self.reactor, self.node, account)
        self.account_set.add_account(account)
        self.account_infos[account] = (dbenv, directory, basename)
        
    def close_wallet(self, account):
        dbenv, directory, basename = self.account_infos[account]
        uid = bsddb_read_file_uid(os.path.join(directory, basename))
        dbenv.open_file_uids.remove(uid)
        self.account_set.remove_account(account)
        del self.account_infos[account]
        
    def start(self):
        self.reactor.start()

    def stop(self, callback):
        self.reactor.stop(callback)
 
    def run(self):
        self.reactor.run()
