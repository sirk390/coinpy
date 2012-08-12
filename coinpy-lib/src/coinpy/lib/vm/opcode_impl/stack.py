# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.lib.vm.stack_valtype import cast_to_number, valtype_from_number,\
    cast_to_bool

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


"""
OP_IFDUP:                   x   ->   x (x)?
    If the top stack value is not 0, duplicate it.
"""
def op_ifdup(vm, instr):
    if len(vm.stack) < 1:
        raise Exception("OP_IFDUP: Not enought arguments")
    if cast_to_bool(vm.stack[-1]):
        vm.stack.append(vm.stack[-1])

"""
OP_DEPTH:                    -> d )
    Pushes the size of the stqck on the top of the stack.
"""
def op_depth(vm, instr):
    vm.stack.append(valtype_from_number(len(vm.stack)))
                   
"""
OP_NIP:                   x1 x2 -> x2 
"""
def op_nip(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_NIP: Not enought arguments")
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack += [x2]

                  
"""
OP_PICK:                  (xn ... x2 x1 x0 n - xn ... x2 x1 x0 xn)
        Pick the element at depths 'n' in the stack and push it on the top
"""
def op_pick(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_PICK: Not enought arguments")
    n = cast_to_number(vm.stack.pop())
    if (n < 0) or (n >= len(vm.stack) ):
        raise Exception("OP_PICK: N is out of range")
    elm = vm.stack[-n-1]
    vm.stack.append(elm)    
                   
"""
OP_ROT:                   x1 x2 x3 -> x2 x3 x1
    Pushes the size of the stqck on the top of the stack.
"""
def op_rot(vm, instr):
    if len(vm.stack) < 3:
        raise Exception("OP_ROT: Not enought arguments")
    x3 = vm.stack.pop()
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack += [x2, x3, x1]

"""
OP_2DUP:                   x1 x2 -> x1 x2 x1 x2
"""
def op_2dup(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_NIP: Not enought arguments")
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack += [x1, x2, x1, x2]

"""
OP_2DROP:                  x1 x2 ->
"""
def op_2drop(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_2DROP: Not enought arguments")
    vm.stack.pop()
    vm.stack.pop()
    
"""
OP_3DUP:                  x1 x2 x3 -> x1 x2 x3 x1 x2 x3
"""
def op_3dup(vm, instr):
    if len(vm.stack) < 3:
        raise Exception("OP_3DUP: Not enought arguments")
    x3 = vm.stack.pop()
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack += [x1, x2, x3, x1, x2, x3]
    
"""
OP_2OVER:                  x1 x2 x3 x4 -> x1 x2 x3 x4 x1 x2       
"""
def op_2over(vm, instr):
    if len(vm.stack) < 4:
        raise Exception("OP_2OVER: Not enought arguments")
    x4 = vm.stack.pop()
    x3 = vm.stack.pop()
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack += [x1, x2, x3, x4, x1, x2]

"""
OP_2ROT:                  x1 x2 x3 x4 x5 x6 -- x3 x4 x5 x6 x1 x2      
"""
def op_2rot(vm, instr):
    if len(vm.stack) < 6:
        raise Exception("OP_2ROT: Not enought arguments")
    x6 = vm.stack.pop()
    x5 = vm.stack.pop()
    x4 = vm.stack.pop()
    x3 = vm.stack.pop()
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack += [x3, x4, x5, x6, x1, x2]


"""
OP_2SWAP:                 x1 x2 x3 x4 -> x3 x4 x1 x2 
"""
def op_2swap(vm, instr):
    if len(vm.stack) < 4:
        raise Exception("OP_2SWAP: Not enought arguments")
    x4 = vm.stack.pop()
    x3 = vm.stack.pop()
    x2 = vm.stack.pop()
    x1 = vm.stack.pop()
    vm.stack += [x3, x4, x1, x2]
                 