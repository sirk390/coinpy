# -*- coding:utf-8 -*-
"""
Created on 13 Aug 2011

@author: kris
"""

from coinpy.model.protocol.structures.uint256 import uint256
class BlockRef():
    def __init__(self, indexdb, blockstorage, hash):
        self.indexdb = indexdb
        self.blockstorage = blockstorage
        self.hash = hash
        self.blockindex = self.indexdb.get_blockindex(self.hash)
        
    def save(self):
        self.indexdb.set_blockindex(self.hash, self.blockindex)

    def is_mainchain(self):
        return (self.blockindex.hash_next == uint256(0) or 
                self.hash == self.indexdb.hashbestchain())

    def get_block(self):
        return (self.blockstorage.load_block(self.blockindex.file, self.blockindex.blockpos))

    def height(self):
        return self.blockindex.height
    
