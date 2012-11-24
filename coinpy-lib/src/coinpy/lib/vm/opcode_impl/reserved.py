from coinpy.model.scripts.opcodes_info import OPCODE_NAMES

def op_not_implemented(vm, instr):
    raise Exception ("Opcode not implemented : %s" % (OPCODE_NAMES[instr.opcode]))

def op_invalid(vm, instr):
    raise Exception ("Opcode invalid: %s" % (OPCODE_NAMES[instr.opcode]))
