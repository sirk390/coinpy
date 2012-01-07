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
from coinpy.model.protocol.structures.block import Block

class block_encoder(Encoder):
    def __init__(self, flags=0):
        self.BLOCK = Structure([blockheader_serializer(flags), 
                                varsizelist_encoder(varint_encoder("txn_count"), tx_encoder())], "block")

    def encode(self, block):
        return (self.BLOCK.encode(block.blockheader,
                                  block.transactions))
        
    def decode(self, data, cursor):
        (blockheader, transactions), cursor = self.BLOCK.decode(data, cursor)
        return (Block(blockheader, transactions), cursor)

