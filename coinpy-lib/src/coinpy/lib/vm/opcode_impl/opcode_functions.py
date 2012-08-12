# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.model.scripts.opcodes import *
from coinpy.lib.vm.opcode_impl.reserved import op_not_implemented, op_invalid
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
    OP_1NEGATE : op_1negate,
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
    OP_NOP : op_nop,
    OP_IF : op_if,
    OP_NOTIF : op_noif,
    OP_ELSE : op_else,
    OP_ENDIF : op_endif,
    OP_VERIFY : op_verify,
    OP_RETURN : op_return,
# Stack 
    OP_TOALTSTACK : op_toaltstack,
    OP_FROMALTSTACK : op_fromaltstack,
    OP_IFDUP : op_ifdup,
    OP_DEPTH : op_depth,
    OP_DROP : op_drop,
    OP_DUP : op_dup,
    OP_NIP : op_nip,
    OP_OVER : op_over,
    OP_PICK : op_pick,
    OP_ROLL : op_roll,
    OP_ROT : op_rot,
    OP_SWAP : op_swap,
    OP_TUCK : op_tuck,
    OP_2DROP : op_2drop,
    OP_2DUP : op_2dup,
    OP_3DUP : op_3dup,
    OP_2OVER : op_2over,
    OP_2ROT : op_2rot,
    OP_2SWAP : op_2swap,
# Splice 
    OP_CAT : op_cat,
    OP_SUBSTR : op_substr,
    OP_LEFT : op_left,
    OP_RIGHT : op_right,
    OP_SIZE : op_size,
# Bitwise logic 
    OP_INVERT : op_not_implemented,
    OP_AND : op_not_implemented,
    OP_OR : op_not_implemented,
    OP_XOR : op_not_implemented,
    OP_EQUAL : op_equal,
    OP_EQUALVERIFY : op_equalverify,
# Arithmetic
    OP_1ADD : op_1add,
    OP_1SUB : op_1sub,
    OP_2MUL : op_2mul,
    OP_2DIV : op_2div,
    OP_NEGATE : op_negate,
    OP_ABS : op_abs,
    OP_NOT : op_not,
    OP_0NOTEQUAL : op_0notequal,
    OP_ADD : op_add,
    OP_SUB : op_sub,
    OP_MUL : op_mul,
    OP_DIV : op_div,
    OP_MOD : op_mod,
    OP_LSHIFT : op_lshift,
    OP_RSHIFT : op_rshift,
    OP_BOOLAND : op_booland,
    OP_BOOLOR : op_boolor,
    OP_NUMEQUAL : op_numequal,
    OP_NUMEQUALVERIFY : op_numequalverify,
    OP_NUMNOTEQUAL : op_numnotequal,
    OP_LESSTHAN : op_lessthan,
    OP_GREATERTHAN : op_greaterthan,
    OP_LESSTHANOREQUAL : op_lessthanorequal,
    OP_GREATERTHANOREQUAL : op_greaterthanorequal,
    OP_MIN : op_min,
    OP_MAX : op_max,
    OP_WITHIN : op_within,
# Crypto 
    OP_RIPEMD160 : op_ripemd160,
    OP_SHA1 : op_sha1,
    OP_SHA256 : op_sha256,
    OP_HASH160 : op_hash160,
    OP_HASH256 : op_hash256,
    OP_CODESEPARATOR : op_nop,
    OP_CHECKSIG : op_checksig,
    OP_CHECKSIGVERIFY : op_checksigverify,
    OP_CHECKMULTISIG : op_checkmultisig,
    OP_CHECKMULTISIGVERIFY : op_checkmultisigverify,
# Pseudo-words 
    OP_PUBKEYHASH : op_invalid,
    OP_PUBKEY : op_invalid,
    OP_INVALIDOPCODE : op_invalid,
# Reserved words
    OP_RESERVED : op_invalid,
    OP_VER : op_invalid,
    OP_VERIF : op_invalid,
    OP_VERNOTIF : op_invalid,
    OP_RESERVED1 : op_invalid,
    OP_RESERVED2 : op_invalid,
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
