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

def op_noif(vm, instr):
    executed = all(vm.cond_stack)
    if executed:
        if (len(vm.stack) < 1):
            raise Exception("OP_NOTIF: Missing argument")
        expr = cast_to_bool(vm.stack.pop())
        vm.cond_stack.append(not expr)
    else:
        vm.cond_stack.append(False)

def op_return(vm, instr):
    raise Exception("OP_RETURN: transaction invalid")

'''
OP_RETURN = 106
'''