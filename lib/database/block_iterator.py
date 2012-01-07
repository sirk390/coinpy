# -*- coding:utf-8 -*-
"""
Created on 13 Aug 2011

@author: kris
"""

from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.model.constants.bitcoin import TARGET_INTERVAL, TARGET_TIMESPAN,\
    PROOF_OF_WORK_LIMIT
from coinpy.lib.bitcoin.difficulty import compact_difficulty

class BlockIterator():
    def __init__(self, log, indexdb, blockstorage, hash, blockindex=None):
        self.log = log
        self.indexdb = indexdb
        self.blockstorage = blockstorage
        self.hash = hash
        self.blockindex = blockindex or self.indexdb.get_blockindex(self.hash)
        
    def save(self):
        self.indexdb.set_blockindex(self.hash, self.blockindex)

    def is_mainchain(self):
        return (self.blockindex.hash_next == uint256(0) or 
                self.hash == self.indexdb.hashbestchain())

    def get_block(self):
        return (self.blockstorage.load_block(self.blockindex.file, self.blockindex.blockpos))

    def height(self):
        return self.blockindex.height
    
    def prev(self):
        self.hash = self.get_blockheader().hash_prev
        self.blockindex = self.indexdb.get_blockindex(self.hash)

    def next(self):
        self.hash = self.blockindex.hash_next
        self.blockindex = self.indexdb.get_blockindex(self.hash)
        
    def get_blockheader(self):
        return (self.blockstorage.load_blockheader(self.blockindex.file, self.blockindex.blockpos))
    
    #ref main.cpp:762
    def get_next_work_required(self):
        if ((self.height() + 1) % TARGET_INTERVAL):
            # Difficulty unchanged
            return (self.get_blockheader().bits)
        
        # Locate the block 2 weeks ago
        it2weekago = BlockIterator(self.log, self.indexdb, self.blockstorage, self.hash, self.blockindex)
        for i in range(TARGET_INTERVAL-1):
            it2weekago.prev()
        header_block2weekago = it2weekago.get_blockheader()
        header_blocknow = self.get_blockheader()
        
        actual_timespan = header_blocknow.time - header_block2weekago.time
        # Limit adjustment step
        if actual_timespan < TARGET_TIMESPAN/4:
            actual_timespan = TARGET_TIMESPAN/4;
        if actual_timespan > TARGET_TIMESPAN*4:
            actual_timespan = TARGET_TIMESPAN*4;

        # Retarget
        new_target = (header_blocknow.target() * actual_timespan / TARGET_TIMESPAN)
        if new_target > PROOF_OF_WORK_LIMIT[self.indexdb.runmode]:
            new_target = PROOF_OF_WORK_LIMIT[self.indexdb.runmode]
        new_bits = compact_difficulty(new_target)
        self.log.info("Retarget: targetTimespan:%d actualTimespan:%d, %08x -> %08x " % (TARGET_TIMESPAN, actual_timespan, header_blocknow.bits, new_bits))
        return (new_bits)
        