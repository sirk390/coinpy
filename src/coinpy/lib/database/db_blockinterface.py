# -*- coding:utf-8 -*-
"""
Created on 13 Aug 2011

@author: kris
"""

from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.model.constants.bitcoin import TARGET_INTERVAL, TARGET_TIMESPAN,\
    PROOF_OF_WORK_LIMIT, MEDIAN_TIME_SPAN
from coinpy.lib.bitcoin.difficulty import compact_difficulty
from coinpy.tools.stat import median
from coinpy.model.blockchain.blockinterface import BlockInterface

class DBBlockInterface(BlockInterface):
    def __init__(self, log, indexdb, blockstorage, hash, blockindex=None):
        self.log = log
        self.indexdb = indexdb
        self.blockstorage = blockstorage
        self.hash = hash
        self.blockindex = blockindex or self.indexdb.get_blockindex(self.hash)

    def is_mainchain(self):
        return (self.blockindex.hash_next == uint256(0) or 
                self.hash == self.indexdb.hashbestchain())

    def get_block(self):
        return (self.blockstorage.load_block(self.blockindex.file, self.blockindex.blockpos))

    def height(self):
        return self.blockindex.height

    def hasprev(self):
        return (self.get_blockheader().hash_prev != uint256(0))

    def prev(self):
        self.hash = self.get_blockheader().hash_prev
        if (self.hash == uint256(0)):
            return (False)
        self.blockindex = self.indexdb.get_blockindex(self.hash)
        return (True)

    def hasnext(self):
        return (self.blockindex.hash_next != uint256(0))

    def next(self):
        self.hash = self.blockindex.hash_next
        self.blockindex = self.indexdb.get_blockindex(self.hash)

    def get_blockheader(self):
        return (self.blockstorage.load_blockheader(self.blockindex.file, self.blockindex.blockpos))
    
    """
        get_next_work_required (see main.cpp:762)
           
            Returns the required work for the next block in the compacted 
            difficulty format (int in the range 0..2**32-1).
            This value must match the 'bits' field of next block's blockheader.
            
            It is recomputed once per TARGET_TIMESPAN (e.g. 2weeks) using 
            the difficulty computation rules. 
    """
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
        new_target = uint256(header_blocknow.target().value * actual_timespan / TARGET_TIMESPAN)
        if new_target > PROOF_OF_WORK_LIMIT[self.indexdb.runmode]:
            new_target = PROOF_OF_WORK_LIMIT[self.indexdb.runmode]
        new_bits = compact_difficulty(new_target)
        self.log.info("Retarget: targetTimespan:%d actualTimespan:%d, %08x -> %08x " % (TARGET_TIMESPAN, actual_timespan, header_blocknow.bits, new_bits))
        return (new_bits)
    
    #ref main.h:1109
    def get_median_time_past(self):
        block_times = []
        iter = BlockIterator(self.log, self.indexdb, self.blockstorage, self.hash, self.blockindex)
        for i in range(MEDIAN_TIME_SPAN):
            block_times.append(iter.get_blockheader().time)
            if (not iter.prev()):
                break;
        return median(block_times)
            