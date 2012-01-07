# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.model.scripts.opcodes import *
from coinpy.model.scripts.instruction import Instruction
from coinpy.tools.bitcoin.base256 import base256encode, base256decode
from coinpy.model.scripts.script import Script

class IntructionSerializer():
    def serialize_pushdata(self, instr):
        datalen = len(instr.data)
        if (OP_PUSHDATA_MIN <= datalen <= OP_PUSHDATA_MAX):
            return (chr(datalen) + instr.data)
        if datalen < (2 ** 8):
            return (chr(OP_PUSHDATA1) + base256encode(datalen, 1) + instr.data)
        if datalen < (2 ** 16):
            return (chr(OP_PUSHDATA2) + base256encode(datalen, 2) + instr.data)
        if datalen < (2 ** 32):
            return (chr(OP_PUSHDATA4) + base256encode(datalen, 4) + instr.data)
        raise Exception("Script file too large")
    
    def deserialize_pushdata(self, data, pos):
        op = ord(data[pos])
        pos += 1
        if (OP_PUSHDATA_MIN <= op <= OP_PUSHDATA_MAX):
            length = op
        if (op == OP_PUSHDATA1):
            length = base256decode(data[pos:pos+1])
            pos += 1
        if (op == OP_PUSHDATA2):
            length = base256decode(data[pos:pos+2]) 
            pos += 2       
        if (op == OP_PUSHDATA2):
            length = base256decode(data[pos:pos+4]) 
            pos += 4   
        return (Instruction(OP_PUSHDATA, data[pos:pos+length]), pos + length)        
    
    def serialize(self, instr):
        if (instr.opcode == OP_PUSHDATA):
            return self.serialize_pushdata(instr)
        return chr(instr.opcode)

    def deserialize(self, data, cursor):
        op = ord(data[cursor])
        if ((OP_PUSHDATA_MIN <= op <= OP_PUSHDATA_MAX) or 
            op == OP_PUSHDATA1 or 
            op == OP_PUSHDATA2 or 
            op == OP_PUSHDATA4):
            return (self.deserialize_pushdata(data, cursor))
        return (Instruction(op), cursor + 1)

class ScriptSerializer():
    def __init__(self):
        self.iser = IntructionSerializer()
        
    def serialize(self, script):
        result = b""
        for i in script.instructions:
            result += self.iser.serialize(i)
        return (result)

    def deserialize(self, data, pos=0):
        l = len(data)
        instructions = []
        while (pos < l):
            instr, pos = self.iser.deserialize(data, pos)
            instructions.append(instr)
        return Script(instructions)
    
