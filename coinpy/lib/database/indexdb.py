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
 
        self.dbenv.open(directory,
                          (DB_CREATE|DB_INIT_LOCK|DB_INIT_LOG|DB_INIT_MPOOL|
                           DB_INIT_TXN|DB_THREAD|DB_RECOVER))
        self.db = bsddb.db.DB(self.dbenv)
        self.dbflags = bsddb.db.DB_THREAD
        
        
        self.txindexserialize = TxIndexSerializer()
        self.blockindex_ser = BlockIndexSerializer()
        
    def open(self):
        self.db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags)
        
    def create(self, genesis_hash, genesis_index):
        self.db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags|bsddb.db.DB_CREATE)
        self.set_blockindex(genesis_hash, genesis_index)
        self.set_hashbestchain(genesis_hash)

    def exists(self):
        return (os.path.isfile(os.path.join(self.directory, self.filename)))

    def contains_transaction(self, transaction_hash):
        return (self.db.has_key("\x02tx" + transaction_hash.to_bytestr()))
    
    def get_transactionindex(self, transaction_hash):
        txindex, cursor = self.txindexserialize.decode(self.db["\x02tx" + transaction_hash.to_bytestr()])
        return txindex
    
    def contains_block(self, block_hash):
        return (self.db.has_key("\x0Ablockindex" + block_hash.to_bytestr()))    

    def set_blockindex(self, blockhash, blockindex):
        blockindex_data = self.blockindex_ser.encode(blockindex)
        self.db["\x0Ablockindex" + blockhash.to_bytestr()] = blockindex_data
        self.db.sync()

    def get_blockindex(self, blockhash):
        blockindex, cursor = self.blockindex_ser.decode(self.db["\x0Ablockindex" + blockhash.to_bytestr()])
        return blockindex

    def set_hashbestchain(self, hash):
        self.db["\x0dhashBestChain"] = hash.to_bytestr()
        self.db.sync()
        
    def get_hashbestchain(self):
        return (uint256.from_bytestr(self.db["\x0dhashBestChain"]))
 
    def hashbestchain(self):
        if not self.db.has_key("\x0dhashBestChain"):
            raise Exception("db error: hashBestChain not found")
        return (uint256.from_bytestr(self.db["\x0dhashBestChain"]))
