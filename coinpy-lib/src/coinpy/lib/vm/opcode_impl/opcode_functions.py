# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.model.scripts.opcodes import *
from coinpy.lib.vm.opcode_impl.reserved import op_not_implemented
from coinpy.lib.vm.opcode_impl.pushdata import * 
from coinpy.lib.vm.opcode_impl.stack import *
from coinpy.lib.vm.opcode_impl.bitwise import*
from coinpy.lib.vm.opcode_impl.flow import *
from coinpy.lib.vm.opcode_impl.crypto import *
from coinpy.lib.vm.opcode_impl.arithmetic import *
from coinpy.lib.vm.opcode_impl.splice import *

OPCODE_FUNCTIONS = {
    OP_0 : op_push_0,
    OP_PUSHDATA : op_pushdata, 
    OP_1NEGATE : op_not_implemented,
    OP_1 : op_push_1_16,
    OP_2 : op_push_1_16,
    OP_3 : op_push_1_16,
    OP_4 : op_push_1_16,
    OP_5 : op_push_1_16,
    OP_6 : op_push_1_16,
    OP_7 : op_push_1_16,
    OP_8 : op_push_1_16,
    OP_9 : op_push_1_16,
    OP_10 : op_push_1_16,
    OP_11 : op_push_1_16,
    OP_12 : op_push_1_16,
    OP_13 : op_push_1_16,
    OP_14 : op_push_1_16,
    OP_15 : op_push_1_16,
    OP_16 : op_push_1_16,
# Flow control 
    OP_NOP : op_not_implemented,
    OP_IF : op_if,
    OP_NOTIF : op_not_implemented,
    OP_ELSE : op_else,
    OP_ENDIF : op_endif,
    OP_VERIFY : op_verify,
    OP_RETURN : op_not_implemented,
# Stack 
    OP_TOALTSTACK : op_toaltstack,
    OP_FROMALTSTACK : op_fromaltstack,
    OP_IFDUP : op_not_implemented,
    OP_DEPTH : op_not_implemented,
    OP_DROP : op_drop,
    OP_DUP : op_dup,
    OP_NIP : op_not_implemented,
    OP_OVER : op_over,
    OP_PICK : op_not_implemented,
    OP_ROLL : op_roll,
    OP_ROT : op_not_implemented,
    OP_SWAP : op_swap,
    OP_TUCK : op_tuck,
    OP_2DROP : op_not_implemented,
    OP_2DUP : op_not_implemented,
    OP_3DUP : op_not_implemented,
    OP_2OVER : op_not_implemented,
    OP_2ROT : op_not_implemented,
    OP_2SWAP : op_not_implemented,
# Splice 
    OP_CAT : op_not_implemented,
    OP_SUBSTR : op_not_implemented,
    OP_LEFT : op_not_implemented,
    OP_RIGHT : op_not_implemented,
    OP_SIZE : op_size,
# Bitwise logic 
    OP_INVERT : op_not_implemented,
    OP_AND : op_not_implemented,
    OP_OR : op_not_implemented,
    OP_XOR : op_not_implemented,
    OP_EQUAL : op_equal,
    OP_EQUALVERIFY : op_equalverify,
# Arithmetic
    OP_1ADD : op_not_implemented,
    OP_1SUB : op_not_implemented,
    OP_2MUL : op_not_implemented,
    OP_2DIV : op_not_implemented,
    OP_NEGATE : op_not_implemented,
    OP_ABS : op_not_implemented,
    OP_NOT : op_not,
    OP_0NOTEQUAL : op_not_implemented,
    OP_ADD : op_add,
    OP_SUB : op_not_implemented,
    OP_MUL : op_not_implemented,
    OP_DIV : op_not_implemented,
    OP_MOD : op_not_implemented,
    OP_LSHIFT : op_not_implemented,
    OP_RSHIFT : op_not_implemented,
    OP_BOOLAND : op_booland,
    OP_BOOLOR : op_boolor,
    OP_NUMEQUAL : op_not_implemented,
    OP_NUMEQUALVERIFY : op_not_implemented,
    OP_NUMNOTEQUAL : op_not_implemented,
    OP_LESSTHAN : op_not_implemented,
    OP_GREATERTHAN : op_not_implemented,
    OP_LESSTHANOREQUAL : op_not_implemented,
    OP_GREATERTHANOREQUAL : op_greaterthanorequal,
    OP_MIN : op_not_implemented,
    OP_MAX : op_not_implemented,
    OP_WITHIN : op_not_implemented,
# Crypto 
    OP_RIPEMD160 : op_not_implemented,
    OP_SHA1 : op_not_implemented,
    OP_SHA256 : op_not_implemented,
    OP_HASH160 : op_hash160,
    OP_HASH256 : op_not_implemented,
    OP_CODESEPARATOR : op_nop,
    OP_CHECKSIG : op_checksig,
    OP_CHECKSIGVERIFY : op_checksigverify,
    OP_CHECKMULTISIG : op_checkmultisig,
    OP_CHECKMULTISIGVERIFY : op_not_implemented,
# Pseudo-words 
    OP_PUBKEYHASH : op_not_implemented,
    OP_PUBKEY : op_not_implemented,
    OP_INVALIDOPCODE : op_not_implemented,
# Reserved words
    OP_RESERVED : op_not_implemented,
    OP_VER : op_not_implemented,
    OP_VERIF : op_not_implemented,
    OP_VERNOTIF : op_not_implemented,
    OP_RESERVED1 : op_not_implemented,
    OP_RESERVED2 : op_not_implemented,
    OP_NOP1 : op_nop,
    OP_NOP2 : op_nop,
    OP_NOP3 : op_nop,
    OP_NOP4 : op_nop,
    OP_NOP5 : op_nop,
    OP_NOP6 : op_nop,
    OP_NOP7 : op_nop,
    OP_NOP8 : op_nop,
    OP_NOP9 : op_nop,
    OP_NOP10 : op_nop    
}
