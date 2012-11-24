from coinpy.lib.database.blockchain.db_blockchain import BSDDbBlockChainDatabase
from coinpy.model.genesis import GENESIS
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
from coinpy.lib.bitcoin.pools.transactionpool import TransactionPool
from coinpy.node.addrpool import AddrPool
from coinpy.node.logic.peer_reconnector import PeerReconnector
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
from coinpy.node.logic.addrpool_filler import AddrPoolFiller
from coinpy.lib.bitcoin.blockchain.blockchain_with_altbranches import BlockchainWithAltbranches
import multiprocessing



class BitcoinClient():
    def __init__(self, log, clientparams): 
        self.clientparams = clientparams
        self.log = log
        self.dbenv_handles = {} 
        self.account_infos = {} # account => (handle, dirname, filename)
        self.dbenv = self.get_dbenv_handle(clientparams.data_directory)
        # Logfile
        handler = logging.handlers.RotatingFileHandler(os.path.join(clientparams.data_directory,clientparams.logfilename), maxBytes=1024*1024*8, backupCount=5)
        self.log.addHandler(handler)
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(fmt)
        # Blockchain
        self.database = BSDDbBlockChainDatabase(self.log, self.dbenv, clientparams.runmode)
        self.database.open_or_create(GENESIS[clientparams.runmode])
        self.blockchain = BlockchainWithAltbranches(self.log, self.database)
        # Transaction Pool
        self.txpool = TransactionPool()
        # Processpool
        self.process_pool = multiprocessing.Pool(multiprocessing.cpu_count())
        # Node
        nodeparams = NodeParams(runmode=clientparams.runmode,
                                port=clientparams.port,
                                version=70000,
                                enabledservices=SERVICES_NODE_NETWORK,
                                nonce=clientparams.nonce,
                                sub_version_num=clientparams.sub_version_num)
        self.node = BitcoinNode(self.blockchain, self.txpool, self.process_pool, nodeparams, self.log)
        # Address Pool
        self.addr_pool = AddrPool()
        # Bootstrapper, AddrPoolFiller
        if clientparams.get("findpeers", True):
            self.bootstrapper = Bootstrapper(clientparams.runmode, self.log)
            self.addrpool_filler = AddrPoolFiller(self.node, self.bootstrapper, self.addr_pool)
        for sockaddr in clientparams.seeds:
            self.addr_pool.addpeer(sockaddr)
        # Reconnector
        self.peer_reconnector = PeerReconnector(self.log, self.node, self.addr_pool, min_connections=clientparams.targetpeers)
        # Wallets
        self.account_set = AccountSet()
        
        
    def get_dbenv_handle(self, directory):
        normdir = os.path.normcase(os.path.normpath(os.path.abspath(directory)))
        if normdir not in self.dbenv_handles:
            self.dbenv_handles[normdir] = BSDDBEnv(normdir)
        return self.dbenv_handles[normdir]
    
    def new_wallet(self, filename, passphrase):
        directory, basename = os.path.split(filename)
        dbenv = self.get_dbenv_handle(directory)
        
        wallet_db = BSDDBWalletDatabase(dbenv, basename)
        wallet_db.create()
        
        wallet = Wallet(wallet_db, self.clientparams.runmode)
        wallet.create(passphrase)
        #add file uid to list
        dbenv.open_file_uids.add(bsddb_read_file_uid(filename))
        
        
        account = WalletAccount(self.log, basename, wallet, self.blockchain)
        TransactionPublisher(self.node, account)
        self.account_set.add_account(account)
        self.account_infos[account] = (dbenv, directory, basename)
            
    def open_wallet(self, filename):
        directory, basename = os.path.split(filename)
        dbenv = self.get_dbenv_handle(directory)
        
        uid = bsddb_read_file_uid(filename)
        if uid in dbenv.open_file_uids:
            raise Exception("Multiple wallets with the same uid unsupported in the same directory.")
        wallet_db = BSDDBWalletDatabase(dbenv, basename)
        wallet = Wallet(wallet_db, self.clientparams.runmode)
        wallet.open()
        account = WalletAccount(self.log, basename, wallet, self.blockchain)
        TransactionPublisher(self.node, account)
        self.account_set.add_account(account)
        self.account_infos[account] = (dbenv, directory, basename)
        #add uid last in case something went wrong before
        dbenv.open_file_uids.add(uid)
        
    def close_wallet(self, account):
        dbenv, directory, basename = self.account_infos[account]
        uid = bsddb_read_file_uid(os.path.join(directory, basename))
        dbenv.open_file_uids.remove(uid)
        self.account_set.remove_account(account)
        del self.account_infos[account]
 