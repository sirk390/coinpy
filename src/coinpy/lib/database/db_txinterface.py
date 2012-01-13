# -*- coding:utf-8 -*-
"""
Created on 13 Jan 2012

@author: kris
"""
from coinpy.model.blockchain.txinterface import TxInterface
from coinpy.lib.bitcoin.hash_block import hash_blockheader
from coinpy.lib.database.db_blockinterface import DBBlockInterface

class DBTxInterface(TxInterface):
    def __init__(self, log, indexdb, blockstorage, hash):
        self.log = log
        self.txindex = self.indexdb.get_blockindex(self.hash)
        self.indexdb = indexdb
        self.blockstorage = blockstorage
        
    def get_transaction(self):
        return (self.blockstorage.load_tx(self.txindex.pos.file, self.txindex.pos.txpos))
    
    def get_block(self):
        blockheader = self.blockstorage.load_blockheader(self.txindex.pos.file, self.txindex.pos.blockpos)
        hash = hash_blockheader(blockheader)
        return DBBlockInterface(self.log, self.indexdb, self.blockstorage, hash)
        
    def is_output_spent(self, output):
        #when spent, CDiskTxPos.File is set to -1, main.h:135 IsNull() 
        return (self.txindex.spent[output].file == -1)
    
    def mark_spent(self, n):        
        pass


'''
class DbTxIterator(TxIterator):
    def __init__(self, indexdb, blockstorage, currenthash):
        self.indexdb = indexdb
        self.blockstorage = blockstorage
        self.seek(currenthash)
        
    def seek(self, hash):
        self.currenthash = hash
        self.currentindex = self.indexdb.get_transactionindex(hash)
        
    def get_tx(self):
        return (self.blockstorage.load_tx(self.currentindex.pos.file, self.currentindex.pos.txpos))
     
    def is_output_spent(self, output):
        #when spent, CDiskTxPos.File is set to -1, main.h:135 IsNull() 
        return (self.txindex.spent[output].file == -1)
    
    def __str__(self):
        return ("DbTxIterator(%s)" % (str(self.currentindex)))
'''