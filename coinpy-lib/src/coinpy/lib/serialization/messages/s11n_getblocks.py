# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.model.protocol.messages.getblocks import msg_getblocks
from coinpy.lib.serialization.structures.s11n_uint256 import uint256_encoder
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder

class getblocks_encoder(Encoder):
    GETBLOCKS = Structure([Field("<I", "version"),              
                           varsizelist_encoder(varint_encoder("count"), uint256_encoder("locator")),
                           uint256_encoder("stop")], "getblocks")
    
    def encode(self, getblocks_msg):
        return (self.GETBLOCKS.encode(getblocks_msg.version,
                                      getblocks_msg.block_locator,
                                      getblocks_msg.hash_stop))

    def decode(self, data, cursor):
        (version, block_locator, hash_stop), cursor = self.GETBLOCKS.decode(data, cursor)
        return (msg_getblocks(version, block_locator, hash_stop), cursor)


    
