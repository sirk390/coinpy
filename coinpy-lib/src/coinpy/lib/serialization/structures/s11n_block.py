# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.model.protocol.messages.block import msg_block
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.model.protocol.structures.block import Block
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer

class BlockSerializer(Serializer):
    def __init__(self, flags=0):
        self.BLOCK = Structure([BlockheaderSerializer(flags), 
                                VarsizelistSerializer(VarintSerializer("txn_count"), TxSerializer())], "block")

    def get_size(self, block):
        return (self.BLOCK.get_size(block.blockheader,
                                    block.transactions))

    def encode(self, block):
        return (self.BLOCK.encode(block.blockheader,
                                  block.transactions))
        
    def decode(self, data, cursor):
        (blockheader, transactions), cursor = self.BLOCK.decode(data, cursor)
        return (Block(blockheader, transactions), cursor)

