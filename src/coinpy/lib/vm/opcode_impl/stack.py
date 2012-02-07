# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.lib.vm.stack_valtype import cast_to_number

"""
OP_DUP:                x -> x x
    Duplicates the top stack item.
"""
def op_dup(vm, instr):
    if not vm.stack:
        raise Exception("OP_DUP: Argument required")
    vm.stack.append(vm.stack[-1])

"""
OP_DROP:                x -> 
    Removes the top stack item. 
"""
def op_drop(vm, instr):
    if not vm.stack:
        raise Exception("OP_DROP: Argument required")
    vm.stack.pop()


"""
OP_TOALTSTACK:            x1 -> (alt)x1  
    Puts the input onto the top of the main stack. 
    Removes it from the alt stack.
"""
def op_toaltstack(vm, instr):
    if not vm.stack:
        raise Exception("OP_TOALTSTACK: Stack empty")
    elm = vm.stack.pop()
    vm.altstack.append(elm)


"""
OP_FROMALTSTACK:         (alt)x1 -> x1
    Puts the input onto the top of the main stack. 
    Removes it from the alt stack.
        
"""
def op_fromaltstack(vm, instr):
    if not vm.altstack:
        raise Exception("OP_FROMALTSTACK: Altstack empty")
    elm = vm.altstack.pop()
    vm.stack.append(elm)


"""
OP_TUCK:                   x1 x2  -> x2 x1 x2
    The item at the top of the stack is copied and inserted before the 
    second-to-top item.
"""
def op_tuck(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_TUCK: Not enought arguments")
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack += [x2, x1, x2]

"""
OP_SWAP:                   x1 x2  -> x2 x1
    The top two items on the stack are swapped.
"""
def op_swap(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_SWAP: Not enought arguments")
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack += [x2, x1]

"""
OP_ROLL:                   xn ... x2 x1 x0 <n>  -> ... x2 x1 x0 xn
    The item n back in the stack is moved to the top.
"""
def op_roll(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_ROLL: Not enought arguments")
    n = cast_to_number(vm.stack.pop())
    if (n < 0) or (n >= len(vm.stack) ):
        raise Exception("OP_ROLL: N is out of range")
    elm = vm.stack[-n-1]
    del vm.stack[-n-1]
    vm.stack.append(elm)

"""
OP_OVER:                   x1 x2  -> x1 x2 x1
    Copies the second-to-top stack item to the top.
"""
def op_over(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_OVER: Not enought arguments")
    vm.stack.append(vm.stack[-2])

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