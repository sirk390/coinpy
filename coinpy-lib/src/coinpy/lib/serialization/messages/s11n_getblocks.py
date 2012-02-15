# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.model.protocol.messages.getblocks import msg_getblocks
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.structures.s11n_blocklocator import BlockLocatorSerializer

class GetBlocksMessageSerializer(Serializer):
    GETBLOCKS = Structure([BlockLocatorSerializer(),
                           Uint256Serializer("stop")], "getblocks")
    
    def serialize(self, getblocks_msg):
        return (self.GETBLOCKS.serialize([getblocks_msg.block_locator,
                                          getblocks_msg.hash_stop]))

    def deserialize(self, data, cursor):
        (block_locator, hash_stop), cursor = self.GETBLOCKS.deserialize(data, cursor)
        return (msg_getblocks(block_locator, hash_stop), cursor)


    
