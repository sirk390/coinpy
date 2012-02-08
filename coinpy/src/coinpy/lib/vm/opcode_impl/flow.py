# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.lib.vm.stack_valtype import cast_to_bool

def op_nop(vm, instr):
    pass

def op_verify(vm, instr):
    if (not vm.stack):
        raise Exception("OP_VERIFY: Missing argument")
    if cast_to_bool(vm.stack[-1]) != True:
        raise Exception("OP_VERIFY: False")
    vm.stack.pop()
    
def op_if(vm, instr):
    executed = all(vm.cond_stack)
    if executed:
        if (len(vm.stack) < 1):
            raise Exception("OP_IF: Missing argument")
        expr = cast_to_bool(vm.stack.pop())
        vm.cond_stack.append(expr)
    else:
        vm.cond_stack.append(False)

def op_else(vm, instr):
    if (len(vm.cond_stack) < 1):
        raise Exception("OP_ELSE: Missing OP_IF")
    vm.cond_stack[-1] = not vm.cond_stack[-1]

def op_endif(vm, instr):
    if (len(vm.cond_stack) < 1):
        raise Exception("OP_ENDIF: Missing OP_IF")
    vm.cond_stack.pop()


'''
OP_NOP = 97
OP_IF = 99
OP_NOTIF = 100
OP_ELSE = 103
OP_ENDIF = 104
OP_VERIFY = 105
OP_RETURN = 106
'''