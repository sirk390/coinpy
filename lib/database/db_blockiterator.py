# -*- coding:utf-8 -*-
"""
Created on 25 Jul 2011

@author: kris
"""
from coinpy.model.blockchain.blockiterator import BlockIterator
import copy
from coinpy.lib.database.blockref import BlockRef

class DbBlockIterator(BlockIterator):
    def __init__(self, indexdb, blockstorage, hash, endhash):
        self.indexdb = indexdb
        self.blockstorage = blockstorage
        self.nexthash = hash
        self.endhash = endhash
        
    def __iter__(self):
        return self

    def next(self):
        if (self.nexthash == None):
            raise StopIteration()
        h = self.nexthash
        self.nexthash = (h != self.endhash) and self.current.blockheader.hash_prev or None
        return (BlockRef(self.blockstorage, h))

    """
    @staticmethod
    def from_hash(indexdb, blockstorage, hash):
        return (DbBlockIterator(indexdb, blockstorage, indexdb.get_blockindex(hash)) )
    
    def copy(self):
        return DbBlockIterator(self.indexdb, self.blockstorage, copy.copy(self.blockindex))
    
    def seek(self, hash):
        self.currenthash = hash
        self.blockindex = self.indexdb.get_blockindex(hash)

    def prev(self):
        self.seek(self.blockindex.blockheader.hash_prev)
    
    def saveindex(self):
        self.indexdb.set_blockindex(self.currenthash, self.blockindex)
        
    def get_block(self):
        return (self.blockstorage.load_block(self.blockindex.file, self.blockindex.blockpos))
    
    def is_mainchain(self):
        return (self.blockindex.hash_next == None or 
                self.blockindex.hash == self.indexdb.hashbestchain())
        
    def mainchain_parent(self):
        while not self.is_mainchain():
            self.prev()

"""
    """    
    def next(self, blockchain):
        if (self.blockindex.hash_next):
            return (self.blockchain.get_block_index(self.hash_next))
        return (None)
    
    def hashprev(self):
        return (self.blockchain.get_block_iterator(self.blockindex.blockheader.hash_prev))
    """

    
    def __str__(self):
        return ("DbIterator(%s)" % (str(self.blockindex)))
