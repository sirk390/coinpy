# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.lib.vm.stack_valtype import valtype_from_number


"""
OP_SIZE:                   x -> len(x)
    Returns the length of the input string.
"""
def op_size(vm, instr):
    if len(vm.stack) < 1:
        raise Exception("OP_SIZE: Not enought arguments")
    vm.stack.append(valtype_from_number(len(vm.stack[-1])))

'''
OP_CAT = 126
OP_SUBSTR = 127
OP_LEFT = 128
OP_RIGHT = 129
OP_SIZE = 130
'''