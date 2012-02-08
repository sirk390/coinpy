# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.model.scripts.opcodes import OP_16, OP_0,\
    OP_PUSHDATA1_75_MIN, OP_PUSHDATA1_75_MAX, OP_PUSHDATA1, OP_PUSHDATA4, OP_PUSHDATA2
from coinpy.model.scripts.opcodes_info import OPCODE_NAMES, is_pushdata
from coinpy.tools.hex import hexstr

class Instruction():
    def __init__(self, opcode, data=None, data_length=None):
        self.opcode = opcode            #value defined in opcodes.py
        self.data = data                #optional (bytestring for pushdata)
        
    def ispush(self):
        return (OP_0 <= self.opcode <= OP_16)

    def __pushdata__str__(self):
        datastr = hexstr(self.data)
        if OP_PUSHDATA1_75_MIN <= self.opcode <= OP_PUSHDATA1_75_MAX:
            return ("OP_PUSHDATA(%d):%s" % (self.opcode, datastr))
        if  self.opcode == OP_PUSHDATA1:
            return ("OP_PUSHDATA1:%s" % (datastr))
        if  self.opcode == OP_PUSHDATA2:
            return ("OP_PUSHDATA2:%s" % (datastr))
        if  self.opcode == OP_PUSHDATA4:
            return ("OP_PUSHDATA4:%s" % (datastr))
        
    def __str__(self):
        if is_pushdata(self.opcode):
            return self.__pushdata__str__()
        if (self.opcode in OPCODE_NAMES):
            return OPCODE_NAMES[self.opcode]
        return ("UNKNOWN(%d)" % self.opcode)