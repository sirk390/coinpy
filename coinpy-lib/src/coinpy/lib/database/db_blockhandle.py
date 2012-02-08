# -*- coding:utf-8 -*-
"""
Created on 13 Aug 2011

@author: kris
"""

from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.model.blockchain.block_handle import BlockHandle


class DBBlockHandle(BlockHandle):
    def __init__(self, log, indexdb, blockstorage, blockhash):
        self.log = log
        self.indexdb = indexdb
        self.blockindex = self.indexdb.get_blockindex(blockhash)
        self.blockstorage = blockstorage
        self.hash = blockhash
           
    def get_block(self):
        return (self.blockstorage.load_block(self.blockindex.file, self.blockindex.blockpos))

    def get_blockheader(self):
        return (self.blockstorage.load_blockheader(self.blockindex.file, self.blockindex.blockpos))

    def get_height(self):
        return self.blockindex.height

    def is_mainchain(self):
        return (self.blockindex.hash_next == uint256(0) or 
                self.hash == self.indexdb.get_hashbestchain())

            