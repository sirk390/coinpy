# -*- coding:utf-8 -*-
"""
Created on 26 Jan 2012

@author: kris
"""
from coinpy.model.constants.bitcoin import TARGET_INTERVAL
class BlockIterator():
    def __init__(self, database, hash):
        self.hash = hash
        self.handle = self.database.get_block_handle(hash)
        
    def get_height(self):
        return self.handle.get_height()
            
    def get_block(self):
        return self.handle.get_block()

    #def hasprev(self):
    #    return (self.get_blockheader().hash_prev != uint256(0))

    def prev(self):
        hash_prev = self.get_blockheader().hash_prev
        self.handle = self.database.get_block_handle(hash_prev)

    #def hasnext(self):
    #    return (self.blockindex.hash_next != uint256(0))
    
    
    #def next(self):
    #    self.hash = self.blockindex.hash_next
    #    self.blockindex = self.indexdb.get_blockindex(self.hash)

    def get_next_work_required(self):
        if ((self.get_height() + 1) % TARGET_INTERVAL):
            # Difficulty unchanged
            return (self.get_blockheader().bits)
        
        # Locate the block 2 weeks ago
        it2weekago = DBBlockInterface(self.log, self.indexdb, self.blockstorage, self.hash, self.blockindex)
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
        iter = DBBlockInterface(self.log, self.indexdb, self.blockstorage, self.hash, self.blockindex)
        for i in range(MEDIAN_TIME_SPAN):
            block_times.append(iter.get_blockheader().time)
            if (not iter.prev()):
                break;
        return median(block_times)
