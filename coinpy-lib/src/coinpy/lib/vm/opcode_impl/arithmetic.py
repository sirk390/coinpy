# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.lib.vm.stack_valtype import cast_to_number, valtype_from_number

def arithmetic_binary_op(vm, func):
    if len(vm.stack) < 2:
        raise Exception("Not enought arguments")
    x2 = cast_to_number(vm.stack.pop())
    x1 = cast_to_number(vm.stack.pop())
    result = func(x1, x2)
    vm.stack.append(valtype_from_number(result))
    
"""
OP_BOOLAND:                    a b  -> a&b
    If both a and b are not 0, the output is 1. Otherwise 0.
"""
def op_booland(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 != 0 and x2 != 0) and 1 or 0)

"""
OP_BOOLAND:                    a b  -> a|b
    If both a and b are not 0, the output is 1. Otherwise 0.
"""
def op_boolor(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 != 0 or x2 != 0) and 1 or 0)

"""
OP_ADD:                        a b  -> a+b
    a is added to b.
"""
def op_add(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: x1 + x2)

"""
OP_GREATERTHANOREQUAL:         a b  -> (a>=b) ? 1 : 0
    Returns 1 if a is greater than or equal to b, 0 otherwise.
"""
def op_greaterthanorequal(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 >= x2) and 1 or 0)

"""
OP_NOT:         a -> !a
    If the input is 0 or 1, it is flipped. Otherwise the output will be 0.
"""
def op_not(vm, instr):
    if len(vm.stack) < 1:
        raise Exception("Not enought arguments")
    x = cast_to_number(vm.stack.pop())
    vm.stack.append(valtype_from_number((x == 0) and 1 or 0))
   
'''
OP_1ADD = 139
OP_1SUB = 140
OP_2MUL = 141
OP_2DIV = 142
OP_NEGATE = 143
OP_ABS = 144
OP_NOT = 145
OP_0NOTEQUAL = 146
OP_ADD = 147
OP_SUB = 148
OP_MUL = 149
OP_DIV = 150
OP_MOD = 151
OP_LSHIFT = 152
OP_RSHIFT = 153
OP_BOOLAND = 154
OP_BOOLOR = 155
OP_NUMEQUAL = 156
OP_NUMEQUALVERIFY = 157
OP_NUMNOTEQUAL = 158
OP_LESSTHAN = 159
OP_GREATERTHAN = 160
OP_LESSTHANOREQUAL = 161
OP_GREATERTHANOREQUAL = 162
OP_MIN = 163
OP_MAX = 164
OP_WITHIN = 165
'''