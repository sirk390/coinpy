# -*- coding:utf-8 -*-
"""
Created on 9 Aug 2011

@author: kris
"""
from copy import copy
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.lib.bitcoin.blockchain.block_iterator import BlockIterator

class Branch():
    def __init__(self, log, database, lasthash, firsthash=None):
        self.log = log
        self.database = database
        self.firsthash = firsthash
        self.lasthash = lasthash
        self.last = BlockIterator(database, lasthash) 

    def is_mainchain(self):
        return (self.last.is_mainchain())

    def work(self):
        return sum(blk.get_blockheader().work() for blk in self)
   
    def get_height(self):
        return self.last.get_height()
            
    def backward_iterblocks(self):
        pos = self.database.get_block_handle(self.lasthash)
        while pos.hasprev() and pos.hash != self.firsthash:
            yield pos
            pos = self.database.get_block_handle(pos.blockindex.blockheader.hash_prev)
            
    def foreward_iterblocks(self):
        #accumulate and reverse hash_prev links (TODO: add a chain length limit)
        blocks = list( self.backward_iterblocks() )
        blocks.reverse()
        for blk in blocks:
            yield blk
            
    def __iter__(self):
        return self.backward_iterblocks()
   