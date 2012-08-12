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

"""
OP_CAT:                   x1 x2 -> x1x2
    Concatenate two elements on the stack
"""
def op_cat(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_CAT: Not enought arguments")
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack.append(x1 + x2)

"""
OP_SUBSTR:                  str start end -> str[start:end]
    Extract a substring
"""
def op_substr(vm, instr):
    if len(vm.stack) < 3:
        raise Exception("OP_SUBSTR: Not enought arguments")
    end = vm.stack.pop()
    begin = vm.stack.pop()
    str = vm.stack.pop()
    vm.stack.append(str[begin:end])


"""
OP_LEFT:                  str n -> str[:n]
    Take the leftmost n characters.
"""
def op_left(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_LEFT: Not enought arguments")
    n = vm.stack.pop()
    str = vm.stack.pop()
    vm.stack.append(str[:n])


"""
OP_RIGHT:                  str n -> str[-n:]
    Take the rightmost n characters.
"""
def op_right(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_RIGHT: Not enought arguments")
    n = vm.stack.pop()
    str = vm.stack.pop()
    vm.stack.append(str[-n:])
