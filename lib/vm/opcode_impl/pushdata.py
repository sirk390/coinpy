# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""

def op_pushdata(vm, instr):
    vm.stack.append(instr.data)

"""
OP_0 = OP_FALSE = 0
OP_1NEGATE = 79
OP_1 = OP_TRUE = 81
OP_2 = 82
OP_3 = 83
OP_4 = 84
OP_5 = 85
OP_6 = 86
OP_7 = 87
OP_8 = 88
OP_9 = 89
OP_10 = 90
OP_11 = 91
OP_12 = 92
OP_13 = 93
OP_14 = 94
OP_15 = 95
OP_16 = 96"""
