# -*- coding:utf-8 -*-
"""
Created on 26 Jul 2011

@author: kris
"""
from coinpy.model.blockchain.txiterator import TxIterator

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
