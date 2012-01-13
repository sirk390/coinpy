# -*- coding:utf-8 -*-
"""
Created on 9 Aug 2011

@author: kris
"""
from coinpy.lib.database.db_blockinterface import DBBlockInterface
from copy import copy


class Branch():
    def __init__(self, log, indexdb, blockstore, lasthash, firsthash=None):
        self.log = log
        self.indexdb = indexdb
        self.blockstore = blockstore
        self.firsthash = firsthash
        self.last = DBBlockInterface(self.log, self.indexdb, self.blockstore, self.lasthash)

    def is_mainchain(self):
        return (self.last.is_mainchain())

    def work(self):
        return sum(blk.blockindex.blockheader.work() for blk in self)
            
    def append(self, blockhash, blockindex):
        #if mainchain maintain hash_next links
        if self.is_mainchain():
            self.last.blockindex.hash_next = blockhash
            self.indexdb.set_blockindex(self.last.hash, self.last.blockindex)
            self.indexdb.set_hashbestchain(blockhash)
        self.last = DBBlockInterface(self.log, self.indexdb, self.blockstore, blockhash)
    '''    
        rework.
    def set_mainchain(self, mainchain=True):
        hashnext = None
        for blk in self:
            blk.blockindex.hash_next = (mainchain and hashnext) or None
            blk.save()
            hashnext = blk.hash
    '''
    def mainchain_parent(self):
        for blk in self:
            if blk.is_mainchain():
                return blk

    def height(self):
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
   