# -*- coding:utf-8 -*-
"""
Created on 7 Aug 2011

@author: kris
"""
from bsddb.db import *
import bsddb
from coinpy.lib.database.blockchain.serialization.s11n_txindex import TxIndexSerializer
from coinpy.lib.database.blockchain.serialization.s11n_blockindex import BlockIndexSerializer
from coinpy.model.protocol.structures.uint256 import uint256
import os
from coinpy.lib.database.bsddb_env import BSDDBEnv

class IndexDB():
    def __init__(self, runmode, bsddb_env, filename="blkindex.dat"):
        self.runmode = runmode
        
        self.txindexserialize = TxIndexSerializer()
        self.blockindex_ser = BlockIndexSerializer()
        self.dbtxn = None
        self.bsddb_env = bsddb_env
        self.filename = filename
        self.db = bsddb.db.DB(self.bsddb_env.dbenv)
        self.dbflags = bsddb.db.DB_THREAD

    def open(self):
        dbtxn = self.bsddb_env.dbenv.txn_begin()
        self.db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags, txn=dbtxn)
        dbtxn.commit()
        
    def create(self, genesis_hash, genesis_index):
        self.dbtxn = self.bsddb_env.dbenv.txn_begin()
        self.db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags|bsddb.db.DB_CREATE, txn=self.dbtxn)
        self.set_blockindex(genesis_hash, genesis_index)
        self.set_hashbestchain(genesis_hash)
        self.dbtxn.commit()

    def exists(self):
        #return (os.path.isfile(os.path.join(self.directory, self.filename)))
        try:
            db = bsddb.db.DB(self.bsddb_env.dbenv)
            db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags)
            db.close()
            return True
        except:
            return False
        
    def begin_updates(self):
        self.dbtxn = self.bsddb_env.dbenv.txn_begin()
        
    def commit_updates(self):
        self.dbtxn.commit()
        #self.db.sync()
        self.dbtxn = None

    def abort_updates(self):
        self.dbtxn.abort()
        self.dbtxn = None
        
    def contains_transaction(self, transaction_hash):
        return (self.db.has_key("\x02tx" + transaction_hash.to_bytestr(), txn=self.dbtxn))
    
    def get_transactionindex(self, transaction_hash):
        txindex_data = self.db.get("\x02tx" + transaction_hash.to_bytestr(), txn=self.dbtxn)
        if not txindex_data:
            raise Exception("txindex not found: %s" % (str(transaction_hash)))
        txindex, _ = self.txindexserialize.deserialize(txindex_data)
        return txindex
 
    def set_transactionindex(self, transaction_hash, txindex):
        self.db.put("\x02tx" + transaction_hash.to_bytestr(), self.txindexserialize.serialize(txindex), txn=self.dbtxn)

    def del_transactionindex(self, transaction_hash):
        self.db.delete("\x02tx" + transaction_hash.to_bytestr(), txn=self.dbtxn)
        
    def contains_block(self, block_hash):
        return (self.db.has_key("\x0Ablockindex" + block_hash.to_bytestr(), txn=self.dbtxn))    

    def set_blockindex(self, blockhash, blockindex):
        blockindex_data = self.blockindex_ser.serialize(blockindex)
        self.db.put("\x0Ablockindex" + blockhash.to_bytestr(), blockindex_data, txn=self.dbtxn)
        #self.db.sync()

    def get_blockindex(self, blockhash):
        blockindex_data = self.db.get("\x0Ablockindex" + blockhash.to_bytestr(), txn=self.dbtxn)
        if not blockindex_data:
            raise Exception("blockindex not found: %s" % (str(blockhash)))
        blockindex, _ = self.blockindex_ser.deserialize(blockindex_data)
        return blockindex

    def set_hashbestchain(self, hash):
        self.db.put("\x0dhashBestChain", hash.to_bytestr(), txn=self.dbtxn)
        
    def get_hashbestchain(self):
        return uint256.from_bytestr(self.db.get("\x0dhashBestChain", txn=self.dbtxn))
 

