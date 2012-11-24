from coinpy.lib.vm.stack_valtype import cast_to_number, valtype_from_number
from coinpy.lib.vm.opcode_impl.flow import op_verify
import functools


def arithmetic_op(vm, func, arity):
    if len(vm.stack) < arity:
        raise Exception("Not enought arguments")
    args = [cast_to_number(vm.stack.pop()) for _ in range(arity)]
    result = func(*reversed(args))
    vm.stack.append(valtype_from_number(result))

arithmetic_unary_op  = functools.partial(arithmetic_op, arity=1)
arithmetic_binary_op = functools.partial(arithmetic_op, arity=2)
arithmetic_ternary_op = functools.partial(arithmetic_op, arity=3)


"""
OP_1ADD:                        a  -> a+1
    1 is added to a.
"""
def op_1add(vm, instr):
    arithmetic_unary_op(vm, lambda a: a + 1)

"""
OP_1SUB:                        a   -> a - 1
    1 is substracted from a.
"""
def op_1sub(vm, instr):
    arithmetic_unary_op(vm, lambda a: a - 1)

"""
OP_2MUL:                        a   -> a * 2
    a is multiplied by 2.
"""
def op_2mul(vm, instr):
    arithmetic_unary_op(vm, lambda a: a * 2)

"""
OP_2DIV:                        a  ->   a / 2
    a is divided by 2.
"""
def op_2div(vm, instr):
    arithmetic_unary_op(vm, lambda a: a / 2)

"""
OP_0NOTEQUAL:                    a  ->    a != 0 ? 1 : 0
    if a is not equal to 0, return 1, otherwise return 0.
"""
def op_0notequal(vm, instr):
    arithmetic_unary_op(vm, lambda x: 1 if (x != 0) else 0)

"""
OP_NEGATE:                        a   ->   -a
    return the opposite of a.
"""
def op_negate(vm, instr):
    arithmetic_unary_op(vm, lambda a: -a)

"""
OP_ABS:                           a    -> (a>0) ? a : -a
    Return the absolute value of a.
"""
def op_abs(vm, instr):
    arithmetic_unary_op(vm, lambda a: abs(a))

"""
OP_NOT:                           a    -> (a==0) ? 1 : -0
    if a equals 0 return 1, otherwise return 0.
"""
def op_not(vm, instr):
    arithmetic_unary_op(vm, lambda a: 1 if a == 0 else 0)
    
"""
OP_0NOTEQUAL:                     a    -> (a!=0) ? 1 : 0
    if a is different than 0 return 1, otherwise return 0.
"""
def op_0noteequal(vm, instr):
    arithmetic_unary_op(vm, lambda a: 0 if a == 0 else 1)

"""
OP_ADD:                        a b  -> a+b
    a is added to b.
"""
def op_add(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: x1 + x2)

"""
OP_SUB:                        a b  -> a-b
    b is subtracted from a.
"""
def op_sub(vm, instr):
    arithmetic_binary_op(vm, lambda a, b: a - b)
    
      
"""
OP_MUL:                        a b  -> a*b
    a is multiplied by b. 
"""
def op_mul(vm, instr):
    arithmetic_binary_op(vm, lambda a, b: a * b)
    
      
"""
OP_DIV:                        a b  -> a/b
    a is divided by b.
"""
def op_div(vm, instr):
    arithmetic_binary_op(vm, lambda a, b: a / b)
"""
OP_MOD:                        a b  -> a%b
    Returns the remainder after dividing a by b.
"""
def op_mod(vm, instr):
    arithmetic_binary_op(vm, lambda a, b: a % b)    
"""
OP_LSHIFT:                        a b  -> a<<b
    Shifts a left b bits, preserving sign.
"""
def op_lshift(vm, instr):
    arithmetic_binary_op(vm, lambda a, b: a << b)    
"""
OP_RSHIFT:                        a b  -> a >> b
    Shifts a right b bits, preserving sign.
"""
def op_rshift(vm, instr):
    arithmetic_binary_op(vm, lambda a, b: a >> b)

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
OP_NUMEQUAL    :         a b  -> (a==b) ? 1 : 0
    Returns 1 if the numbers are equal, 0 otherwise.
"""
def op_numequal(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 == x2) and 1 or 0)

"""
OP_NUMEQUALVERIFY:         a b  -> (a==b) ? 1 : 0
    Same as OP_NUMEQUAL, but runs OP_VERIFY afterward.
"""
def op_numequalverify(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 == x2) and 1 or 0)
    op_verify(vm, instr)
    
"""
OP_NUMEQUAL    :         a b  -> (a!=b) ? 1 : 0
    Returns 1 if the numbers are equal, 0 otherwise.
"""
def op_numnotequal(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 != x2) and 1 or 0)

    
"""
OP_LESSTHAN    :         a b  -> (a<b) ? 1 : 0
    Returns 1 if a is less than b, 0 otherwise.
"""
def op_lessthan(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 < x2) and 1 or 0)

    
"""
OP_GREATERTHAN    :         a b  -> (a>b) ? 1 : 0
    Returns 1 if a is less than b, 0 otherwise.
"""
def op_greaterthan(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 > x2) and 1 or 0)
    

"""
OP_LESSTHANOREQUAL    :         a b  -> (a<=b) ? 1 : 0
    Returns 1 if a is less than or equal to b, 0 otherwise.
"""
def op_lessthanorequal(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 <= x2) and 1 or 0)


"""
OP_GREATERTHANOREQUAL:         a b  -> (a>=b) ? 1 : 0
    Returns 1 if a is greater than or equal to b, 0 otherwise.
"""
def op_greaterthanorequal(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: (x1 >= x2) and 1 or 0)


"""
OP_MIN:         a b  -> min(a, b)
    Returns the smaller of a and b.
"""
def op_min(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: min(x1, x2))

"""
OP_MAX:         a b  -> max(a, b)
    Returns the smaller of a and b.
"""
def op_max(vm, instr):
    arithmetic_binary_op(vm, lambda x1,x2: max(x1, x2))

"""
OP_WITHIN:         x min max  -> (min <= x < max) ? 1 : 0
     Returns 1 if x is within the specified range (left-inclusive), 0 otherwise.
"""
def op_within(vm, instr):
    arithmetic_ternary_op(vm, lambda x, min, max: 1 if (min <= x < max) else 0)

