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
from coinpy.lib.database.objects.txindex import DbTxIndex
from coinpy.lib.serialization.structures.s11n_blockheader import blockheader_serializer
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.lib.bitcoin.hash_tx import hash_tx

class DBBlockHandle(BlockInterface):
    def __init__(self, log, indexdb, blockindex, blockstorage, hash):
        self.log = log
        self.indexdb = indexdb
        self.blockindex = blockindex
        self.blockstorage = blockstorage
        self.hash = hash
           
    def get_block(self):
        return (self.blockstorage.load_block(self.blockindex.file, self.blockindex.blockpos))

    def get_blockheader(self):
        return (self.blockstorage.load_blockheader(self.blockindex.file, self.blockindex.blockpos))

    def get_height(self):
        return self.blockindex.height

    def is_mainchain(self, hash):
        return (self.blockindex.hash_next == uint256(0) or 
                hash == self.indexdb.hashbestchain())

            