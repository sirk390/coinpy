from coinpy.model.scripts.opcodes import OP_PUSHDATA1, OP_PUSHDATA1_75_MAX,\
    OP_PUSHDATA1_75_MIN, OP_PUSHDATA4, OP_PUSHDATA2, OP_0, OP_1
from coinpy.model.scripts.instruction import Instruction
from coinpy.lib.vm.stack_valtype import valtype_from_number

# push_data_instruction: 
#    use the best opcode for the PUSH_DATA depending on len(data)
def push_data_instruction(data):
    l = len(data)
    if l == 0:
        return Instruction(OP_0)
    elif OP_PUSHDATA1_75_MIN <= l <= OP_PUSHDATA1_75_MAX:
        return Instruction(l, data)
    elif l < 0xff:
        return Instruction(OP_PUSHDATA1, data)
    elif l < 0xffff:
        return Instruction(OP_PUSHDATA2, data)
    return Instruction(OP_PUSHDATA4, data)

def push_bignum_instruction(bn):
    return push_data_instruction(valtype_from_number(bn))

def push_smallint(i):
    return Instruction(OP_1 + i - 1)
