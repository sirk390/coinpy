# -*- coding:utf-8 -*-
"""
Created on 17 Nov 2011

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.tools.bitcoin.sha256 import doublesha256

BLOCK_SERIALIZE = BlockheaderSerializer()

    
def hash_blockheader(blockheader):
    return (uint256.from_bytestr(doublesha256(BLOCK_SERIALIZE.serialize(blockheader))))
    
def hash_block(block):
    return (hash_blockheader(block.blockheader))



