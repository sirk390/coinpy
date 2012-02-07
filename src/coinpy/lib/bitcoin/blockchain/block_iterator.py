# -*- coding:utf-8 -*-
"""
Created on 26 Jan 2012

@author: kris
"""
from coinpy.model.constants.bitcoin import TARGET_INTERVAL, TARGET_TIMESPAN,\
    PROOF_OF_WORK_LIMIT, MEDIAN_TIME_SPAN
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.bitcoin.difficulty import compact_difficulty
from coinpy.tools.stat import median

class BlockIterator():
    def __init__(self, database, hash):
        self.database = database
        self.hash = hash
        self.handle = self.database.get_block_handle(hash)
        
    def get_height(self):
        return self.handle.get_height()

    def is_mainchain(self):
        return self.handle.is_mainchain()
    
    def get_handle(self):
        return self.handle
    
    def get_block(self):
        return self.handle.get_block()

    def get_blockheader(self):
        return self.handle.get_blockheader()

    def hasprev(self):
        return (self.hash != self.database.genesis_hash)

    def prev(self):
        self.hash = self.get_blockheader().hash_prev
        self.handle = self.database.get_block_handle(self.hash)

    def get_next_work_required(self):
        if ((self.get_height() + 1) % TARGET_INTERVAL):
            # Difficulty unchanged
            return (self.get_blockheader().bits)
        
        # Locate the block 2 weeks ago
        it2weekago = BlockIterator(self.database, self.hash)
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
        #TODO replace with "branch"
        iter = BlockIterator(self.database, self.hash)
        for dummy in range(MEDIAN_TIME_SPAN):
            block_times.append(iter.get_blockheader().time)
            if (not iter.prev()):
                break;
        return median(block_times)
