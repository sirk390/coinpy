# -*- coding:utf-8 -*-
"""
Created on 9 Aug 2011

@author: kris
"""
from coinpy.lib.database.block_iterator import BlockIterator

class Branch():
    def __init__(self, log, indexdb, blockstore, lasthash, firsthash=None):
        self.log = log
        self.indexdb = indexdb
        self.blockstore = blockstore
        self.lasthash = lasthash
        self.firsthash = firsthash
        
        self.last = BlockIterator(self.log, self.indexdb, self.blockstore, self.lasthash)
        #self.blockindex = self.indexdb.get_blockindex(lasthash)

    def is_mainchain(self):
        return (self.last.is_mainchain())

    def work(self):
        return sum(blk.blockindex.blockheader.work() for blk in self)
            
    def append(self, blockhash, blockindex):
        if self.is_mainchain:
            self.last.blockindex.hash_next = blockhash
            self.last.save()
            self.indexdb.set_hashbestchain(blockhash)
        #increment height and set new last
        height = self.last.blockindex.height
        self.last = BlockIterator(self.log, self.indexdb, self.blockstore, blockhash)
        #self.last.blockindex.height = height + 1
        #self.last.save()
        self.lasthash = blockhash
        
    def set_mainchain(self, mainchain=True):
        hashnext = None
        for blk in self:
            blk.blockindex.hash_next = (mainchain and hashnext) or None
            blk.save()
            hashnext = blk.hash
            
    def mainchain_parent(self):
        for blk in self:
            if blk.is_mainchain():
                return blk

    def height(self):
        return self.last.blockindex.height
            
#    def __iter__(self):
#        return DbBlockIterator(self.indexdb, self.blockstore, self.ref.hash, self.firsthash)
    
"""     
        self.blockindex = self.indexdb.get_blockindex(lasthash)
        
    def is_mainchain(self):
        return (self.blockindex.hash_next == None or 
                self.blockindex.hash == self.indexdb.hashbestchain())
    
    """