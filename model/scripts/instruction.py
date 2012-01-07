# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.model.scripts.opcodes import OP_PUSHDATA, OP_16, OP_0
from coinpy.model.scripts.opcodes_info import OPCODE_NAMES

class Instruction():
    def __init__(self, opcode, data=None):
        self.opcode = opcode    #value defined in opcodes.py
        self.data = data        #optional (bytestring for pushdata)
        
    def ispush(self):
        return (OP_0 <= self.opcode <= OP_16)

    def __str__(self):
        if (self.opcode == OP_PUSHDATA):
            #return ("OP_PUSHDATA(%d:%s...]" % (len(self.data), "".join("%02x" % ord(c) for c in self.data[:4])))
            return ("OP_PUSHDATA(%d:%s...]" % (len(self.data), "".join("%02x" % ord(c) for c in self.data)))
        if (self.opcode in OPCODE_NAMES):
            return OPCODE_NAMES[self.opcode]
        return ("UNKNOWN(%d)" % self.opcode)
