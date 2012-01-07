# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.model.protocol.messages.block import msg_block
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.lib.serialization.messages.s11n_tx import tx_encoder
from coinpy.lib.serialization.structures.s11n_uint256 import uint256_encoder
from coinpy.lib.serialization.structures.s11n_blockheader import blockheader_serializer
from coinpy.lib.serialization.structures.s11n_block import block_encoder

class block_msg_encoder(Encoder):
    block_encoder = block_encoder()
    
    def __init__(self):    
        pass     
                                                      
    def encode(self, block_msg):
        return (self.block_encoder.encode(block_msg.block))
        
    def decode(self, data, cursor):
        block, cursor = self.block_encoder.decode(data, cursor)
        return (msg_block(block), cursor)

