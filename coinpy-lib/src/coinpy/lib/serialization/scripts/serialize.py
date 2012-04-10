# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.model.scripts.opcodes import *
from coinpy.model.scripts.instruction import Instruction
from coinpy.tools.bitcoin.base256 import base256encode, base256decode
from coinpy.model.scripts.script import Script, RawScript
from coinpy.model.scripts.opcodes_info import is_pushdata
from coinpy.lib.serialization.exceptions import MissingDataException
from coinpy.lib.serialization.common.serializer import Serializer

class IntructionSerializer(Serializer):
    """
        Deserialisation + serialisation shouldn't change opcodes even 
        in case of errors in the script.
        
        E.g. on testnet some scripts have opcode OP_PUSHDATA(1-75) but not 
        enough data following. It is possible to have an instruction
        OP_PUSHDATA(1-75) with a different pushed data length. 
    """
    def serialize_pushdata(self, instr):
        if (OP_PUSHDATA1_75_MIN <= instr.opcode <= OP_PUSHDATA1_75_MAX):
            return (chr(instr.opcode) + instr.data)
        if instr.opcode == OP_PUSHDATA1: 
            return (chr(instr.opcode) + base256encode(len(instr.data), pad=1) + instr.data)
        if instr.opcode == OP_PUSHDATA2:
            return (chr(instr.opcode) + base256encode(len(instr.data), pad=2) + instr.data)
        if instr.opcode == OP_PUSHDATA4:
            return (chr(instr.opcode) + base256encode(len(instr.data), pad=4) + instr.data)
        raise Exception("Unknown PUSHDATA opcode")
    
    def _get_size_pushdata(self, instr):
        if (OP_PUSHDATA1_75_MIN <= instr.opcode <= OP_PUSHDATA1_75_MAX):
            return (1 + instr.opcode)
        if instr.opcode == OP_PUSHDATA1: 
            return (1 + 1 + len(instr.data))
        if instr.opcode == OP_PUSHDATA2:
            return (1 + 2+ len(instr.data))
        if instr.opcode == OP_PUSHDATA4:
            return (1 + 4+ len(instr.data))
        raise Exception("Unknown PUSHDATA opcode")
        
    def _deserialize_pushdata_data(self, op, datalength, data, pos):
        if (len(data) < pos + datalength):
            raise MissingDataException("pushdata data")
        return (Instruction(op, data[pos:pos+datalength]), pos+datalength)
    
    def _deserialize_pushdata_length_and_data(self, op, data, pos):
        lenlen = {OP_PUSHDATA1:1, OP_PUSHDATA2:2, OP_PUSHDATA4:4}[op]
        if (len(data) < pos + lenlen):
            raise MissingDataException("pushdata length size")
        length = base256decode(data[pos:pos+lenlen])
        return (self._deserialize_pushdata_data(op, length, data, pos + lenlen))
        
    def _deserialize_pushdata(self, data, pos):
        op = ord(data[pos])
        pos += 1
        if (OP_PUSHDATA1_75_MIN <= op <= OP_PUSHDATA1_75_MAX):
            instr, pos = self._deserialize_pushdata_data(op, op, data, pos)
        if (op == OP_PUSHDATA1 or op == OP_PUSHDATA2 or op == OP_PUSHDATA4):
            instr, pos = self._deserialize_pushdata_length_and_data(op, data, pos)
        return (instr, pos)
       
    
    def serialize(self, instr):
        if is_pushdata(instr.opcode):
            return self.serialize_pushdata(instr)
        return chr(instr.opcode)
    
    def get_size(self, instr):
        if is_pushdata(instr.opcode):
            return self._get_size_pushdata(instr)
        return 1
    
    def deserialize(self, data, cursor):
        op = ord(data[cursor])
        if is_pushdata(op):
            return (self._deserialize_pushdata(data, cursor))
        return (Instruction(op), cursor + 1)

class ScriptSerializer():
    def __init__(self):
        self.iser = IntructionSerializer()
        
    def serialize(self, script):
        if type(script) is RawScript:
            return script.data
        return ("".join(self.iser.serialize(i) for i in script.instructions))
    
    def get_size(self, script):
        if type(script) is RawScript:
            return len(script.data)
        return sum(self.iser.get_size(i) for i in script.instructions)
    
    def deserialize(self, data, pos=0):
        try:
            l = len(data)
            instructions = []
            while (pos < l):
                instr, pos = self.iser.deserialize(data, pos)
                instructions.append(instr)
            return Script(instructions)
        except:
            return RawScript(data)
        
    
