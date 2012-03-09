# -*- coding:utf-8 -*-
"""
Created on 6 Mar 2012

@author: kris
"""
from coinpy.model.scripts.opcodes import OP_CHECKSIG, OP_DUP, OP_EQUALVERIFY,\
    OP_HASH160, OP_PUSHDATA
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.script import Script

SCRIPT_PUBKEYHASH_OPCODES = [OP_DUP, OP_HASH160, OP_PUSHDATA, OP_EQUALVERIFY, OP_CHECKSIG]

def make_script_pubkeyhash(pubkey_hash):
    instructions = [Instruction(OP_DUP),
                    Instruction(OP_HASH160),
                    Instruction(OP_PUSHDATA, data=pubkey_hash),
                    Instruction(OP_EQUALVERIFY),
                    Instruction(OP_CHECKSIG)]
    return Script(instructions)

def make_script_pubkeyhash_sig(pubkey, sig):
    return Script([Instruction(OP_PUSHDATA, data=sig),
                   Instruction(OP_PUSHDATA, data=pubkey)])  

