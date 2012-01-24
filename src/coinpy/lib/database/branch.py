# -*- coding:utf-8 -*-
"""
Created on 9 Aug 2011

@author: kris
"""
from coinpy.lib.database.db_blockinterface import DBBlockInterface
from copy import copy
from coinpy.model.protocol.structures.uint256 import uint256


class Branch():
    def __init__(self, log, indexdb, blockstore, lasthash, firsthash=None):
        self.log = log
        self.indexdb = indexdb
        self.blockstore = blockstore
        self.firsthash = firsthash
        self.lasthash = lasthash
        self.last = DBBlockInterface(self.log, self.indexdb, self.blockstore, self.lasthash)

    def is_mainchain(self):
        return (self.last.is_mainchain())

    def work(self):
        return sum(blk.blockindex.blockheader.work() for blk in self)
    
    def append(self, blockinterface):
        blockhash = blockinterface.get_hash()
        #if mainchain maintain hash_next link for the preceding item
        if self.is_mainchain():
            self.last.blockindex.hash_next = blockhash
            self.indexdb.set_blockindex(self.last.hash, self.last.blockindex)
            self.indexdb.set_hashbestchain(blockhash)
            #index transactions
            blockinterface.index_transactions()
        self.last = blockinterface

    def set_mainchain(self):
        next = uint256(0)
        for blk in self.backward_iterblocks():
            blk.set_next(next)
            blk.index_transactions()
            next = blk 

    def set_altchain(self):
        for blk in self.backward_iterblocks():
            blk.set_next(uint256(0))
            blk.a()

    def mainchain_parent(self):
        for blk in self:
            if blk.is_mainchain():
                return blk

    def get_height(self):
        return self.last.blockindex.height
            
    def backward_iterblocks(self):
        pos, completed = copy(self.last), False
        while not completed:
            yield pos
            completed = (not pos.prev() or pos.hash == self.firsthash)

    def foreward_iterblocks(self):
        #in mainchain use hash_next
        if self.is_mainchain():
            pos = copy(self.first)
            while (pos.hash != self.lasthash):
                yield pos
                pos.next()
        else:
        #in altchains accumulate and reverse hash_prev links (TODO: add a chain length limit)
            for block in list( self.backward_iterblocks() ).reverse:
                yield block
            
    def __iter__(self):
        return self.backward_iterblocks()
   