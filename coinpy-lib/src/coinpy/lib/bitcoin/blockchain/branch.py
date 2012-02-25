# -*- coding:utf-8 -*-
"""
Created on 9 Aug 2011

@author: kris
"""
from copy import copy
from coinpy.model.protocol.structures.uint256 import uint256
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
        pos = BlockIterator(self.database, self.lasthash) 
        while pos.hasprev() and pos.hash != self.firsthash and pos.hash != uint256.zero():
            yield pos
            pos.prev()
        yield pos
            
    def foreward_iterblocks(self):
        #accumulate and reverse hash_prev links (TODO: add a chain length limit)
        for block in list( self.backward_iterblocks() ).reverse:
            yield block
            
    def __iter__(self):
        return self.backward_iterblocks()
   