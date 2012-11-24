from coinpy.model.scripts.opcodes import OP_PUSHDATA1, OP_PUSHDATA1_75_MAX,\
    OP_PUSHDATA1_75_MIN, OP_PUSHDATA4, OP_PUSHDATA2
from coinpy.model.scripts.instruction import Instruction

# auto_push_data_instruction: 
#    use the best opcode for the PUSH_DATA depending on len(data)
def auto_push_data_instruction(data):
    l = len(data)
    if OP_PUSHDATA1_75_MIN <= l <= OP_PUSHDATA1_75_MAX:
        return Instruction(l, data)
    elif l < 0xff:
        return Instruction(OP_PUSHDATA1, data)
    elif l < 0xffff:
        return Instruction(OP_PUSHDATA2, data)
    return Instruction(OP_PUSHDATA4, data)