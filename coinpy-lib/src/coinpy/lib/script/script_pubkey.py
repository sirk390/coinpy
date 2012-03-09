# -*- coding:utf-8 -*-
"""
Created on 6 Mar 2012

@author: kris
"""
from coinpy.model.scripts.opcodes import OP_CHECKSIG, OP_PUSHDATA
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.script import Script

SCRIPT_PUBKEY_OPCODES = [OP_PUSHDATA, OP_CHECKSIG]

def make_script_pubkey(pubkey):
    instructions = [Instruction(OP_PUSHDATA, data=pubkey),
                    Instruction(OP_CHECKSIG)]
    return Script(instructions)

def make_script_pubkey_sig(sig):
    return Script([Instruction(OP_PUSHDATA, data=sig)])  

