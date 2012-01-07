# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""

def op_dup(vm, instr):
    if not vm.stack:
        raise Exception("OP_DUP: Argument required")
    vm.stack.append(vm.stack[-1])

'''
OP_TOALTSTACK = 107
OP_FROMALTSTACK = 108
OP_IFDUP = 115
OP_DEPTH = 116
OP_DROP = 117
OP_DUP = 118
OP_NIP = 119
OP_OVER = 120
OP_PICK = 121
OP_ROLL = 122
OP_ROT = 123
OP_SWAP = 124
OP_TUCK = 125
OP_2DROP = 109
OP_2DUP = 110
OP_3DUP = 111
OP_2OVER = 112
OP_2ROT = 113
OP_2SWAP = 114'''