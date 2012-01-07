# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.model.scripts.vm.opcode_impl.flow import op_verify

def op_equal(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_EQUAL: Insufficient Arguments")
    first, second = vm.stack.pop(), vm.stack.pop()
    vm.stack.append(first == second)

def op_equalverify(vm, instr):
    op_equal(vm, instr)
    op_verify(vm, instr)

'''
OP_INVERT = 131
OP_AND = 132
OP_OR = 133
OP_XOR = 134
OP_EQUAL = 135
OP_EQUALVERIFY = 136

'''