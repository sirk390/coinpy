# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.model.protocol.messages.block import msg_block
from coinpy.lib.serialization.structures.s11n_block import BlockSerializer

class BlockMessageSerializer(Serializer):
    block_encoder = BlockSerializer()
    
    def __init__(self):    
        pass     
                                                      
    def encode(self, block_msg):
        return (self.block_encoder.encode(block_msg.block))
        
    def decode(self, data, cursor):
        block, cursor = self.block_encoder.decode(data, cursor)
        return (msg_block(block), cursor)

