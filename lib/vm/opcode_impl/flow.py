# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
def op_nop(vm, instr):
    pass

def op_verify(vm, instr):
    if (not vm.stack):
        raise Exception("OP_VERIFY: Missing argument")
    if vm.stack[-1] != True:
        raise Exception("OP_VERIFY: False")
    vm.stack.pop()
    

'''
OP_NOP = 97
OP_IF = 99
OP_NOTIF = 100
OP_ELSE = 103
OP_ENDIF = 104
OP_VERIFY = 105
OP_RETURN = 106
'''