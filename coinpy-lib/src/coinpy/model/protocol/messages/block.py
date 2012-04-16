# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_BLOCK
from coinpy.model.protocol.messages.message import Message
from coinpy.model.protocol.structures.block import Block

class BlockMessage(Message):
    def __init__(self, block):
        message.__init__(self, MSG_BLOCK)
        self.block = block
        
    def __str__(self):
        return ("msg_block(%s)" % (str(self.block)))
