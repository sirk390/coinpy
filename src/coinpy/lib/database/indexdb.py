# -*- coding:utf-8 -*-
"""
Created on 7 Aug 2011

@author: kris
"""
from bsddb.db import *
import bsddb
from coinpy.lib.database.serialization.s11n_txindex import TxIndexSerializer
from coinpy.lib.database.serialization.s11n_blockindex import BlockIndexSerializer
from coinpy.model.protocol.structures.uint256 import uint256
import os

class IndexDB():
    def __init__(self, runmode, directory=".", filename="blkindex.dat"):
        self.runmode = runmode
        self.directory = directory
        self.filename = filename
        self.dbenv = bsddb.db.DBEnv()
        
        self.dbenv.set_lg_max(10000000)
        self.dbenv.set_lk_max_locks(10000)
        self.dbenv.set_lk_max_objects(10000)
        self.dbenv.open(directory,
                          DB_CREATE|DB_INIT_LOCK|DB_INIT_LOG|DB_INIT_MPOOL|
                           DB_INIT_TXN|DB_THREAD|DB_RECOVER)
        self.db = bsddb.db.DB(self.dbenv)
        self.dbflags = bsddb.db.DB_THREAD
        
        
        self.txindexserialize = TxIndexSerializer()
        self.blockindex_ser = BlockIndexSerializer()
        self.dbtxn = None
        
    def begin_updates(self):
        self.dbtxn = self.dbenv.txn_begin()
        
    def commit_updates(self):
        self.dbtxn.commit()
        #self.db.sync()
        self.dbtxn = None

    def abort_updates(self):
        self.dbtxn.abort()
        self.dbtxn = None

    def open(self):
        dbtxn = self.dbenv.txn_begin()
        self.db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags, txn=dbtxn)
        dbtxn.commit()
        
    def create(self, genesis_hash, genesis_index):
        self.dbtxn = self.dbenv.txn_begin()
        self.db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags|bsddb.db.DB_CREATE, txn=self.dbtxn)
        self.set_blockindex(genesis_hash, genesis_index)
        self.set_hashbestchain(genesis_hash)
        self.dbtxn.commit()

    def exists(self):
        #return (os.path.isfile(os.path.join(self.directory, self.filename)))
        try:
            db = bsddb.db.DB(self.dbenv)
            db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags)
            db.close()
            return True
        except:
            return False
        
    def contains_transaction(self, transaction_hash):
        return (self.db.has_key("\x02tx" + transaction_hash.to_bytestr(), txn=self.dbtxn))
    
    def get_transactionindex(self, transaction_hash):
        txindex_data = self.db.get("\x02tx" + transaction_hash.to_bytestr(), txn=self.dbtxn)
        if not txindex_data:
            raise Exception("txindex not found: %s" % (str(transaction_hash)))
        txindex, _ = self.txindexserialize.decode(txindex_data)
        return txindex
 
    def set_transactionindex(self, transaction_hash, txindex):
        self.db.put("\x02tx" + transaction_hash.to_bytestr(), self.txindexserialize.encode(txindex), txn=self.dbtxn)

    def del_transactionindex(self, transaction_hash):
        self.db.delete("\x02tx" + transaction_hash.to_bytestr(), txn=self.dbtxn)
        
    def contains_block(self, block_hash):
        return (self.db.has_key("\x0Ablockindex" + block_hash.to_bytestr(), txn=self.dbtxn))    

    def set_blockindex(self, blockhash, blockindex):
        blockindex_data = self.blockindex_ser.encode(blockindex)
        self.db.put("\x0Ablockindex" + blockhash.to_bytestr(), blockindex_data, txn=self.dbtxn)
        #self.db.sync()

    def get_blockindex(self, blockhash):
        blockindex_data = self.db.get("\x0Ablockindex" + blockhash.to_bytestr(), txn=self.dbtxn)
        if not blockindex_data:
            raise Exception("txindex not found: %s" % (str(blockhash)))
        blockindex, _ = self.blockindex_ser.decode(blockindex_data)
        return blockindex

    def set_hashbestchain(self, hash):
        self.db.put("\x0dhashBestChain", hash.to_bytestr(), txn=self.dbtxn)
        
    def get_hashbestchain(self):
        return uint256.from_bytestr(self.db.get("\x0dhashBestChain", txn=self.dbtxn))
 

