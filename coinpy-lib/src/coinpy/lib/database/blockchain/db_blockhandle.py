# -*- coding:utf-8 -*-
"""
Created on 13 Aug 2011

@author: kris
"""

from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.model.blockchain.block_handle import BlockHandle


class DBBlockHandle(BlockHandle):
    def __init__(self, log, indexdb, blockstorage, blockhash, block=None):
        self.log = log
        self.indexdb = indexdb
        self.blockindex = self.indexdb.get_blockindex(blockhash)
        self.blockstorage = blockstorage
        self.hash = blockhash
        #cache
        self.block = block
           
    def get_block(self):
        if not self.block:
            self.block = self.blockstorage.load_block(self.blockindex.file, self.blockindex.blockpos)
        return (self.block)

    def get_blockheader(self):
        return self.blockindex.blockheader
        #return (self.blockstorage.load_blockheader(self.blockindex.file, self.blockindex.blockpos))
    
    def get_height(self):
        return self.blockindex.height

    def is_mainchain(self):
        return (self.blockindex.hash_next != uint256.zero() or 
                self.hash == self.indexdb.get_hashbestchain())

    def hasprev(self):
        return self.blockindex.blockheader.hash_prev != uint256.zero()
    

    def __eq__(self, other):
        return self.hash == other.hash
    