from coinpy.model.scripts.opcodes import OP_CHECKSIG, OP_PUSHDATA
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.script import Script
from coinpy.lib.vm.script.push_data import push_data_instruction

SCRIPT_PUBKEY_OPCODES = [OP_PUSHDATA, OP_CHECKSIG]

def make_script_pubkey(pubkey):
    instructions = [push_data_instruction(data=pubkey),
                    Instruction(OP_CHECKSIG)]
    return Script(instructions)

def make_script_pubkey_sig(sig):
    return Script([push_data_instruction(data=sig)])  

