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
        return (self.handle.hasprev())

    def prev(self):
        self.hash = self.get_blockheader().hash_prev
        self.handle = self.database.get_block_handle(self.hash)


