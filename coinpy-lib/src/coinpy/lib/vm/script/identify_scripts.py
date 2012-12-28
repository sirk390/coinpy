from coinpy.model.scripts.opcodes import OP_PUSHDATA
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY,\
    TX_SCRIPTHASH
from coinpy.model.scripts.opcodes_info import is_pushdata
from coinpy.lib.vm.script.standard_scripts import SCRIPT_P2SH_OPCODES,\
    SCRIPT_PUBKEYHASH_OPCODES, SCRIPT_PUBKEY_OPCODES



def normalize_pushdata(opcodes):
    return [(is_pushdata(op) and OP_PUSHDATA or op) for op in opcodes]

""" 
    Identifies a standard script type:    
        returns one of (TX_PUBKEY, TX_PUBKEYHASH, TX_MULTISIG, TX_SCRIPTHASH) 
                     or None if not found.
"""
def identify_script(script):
    opcodes = normalize_pushdata(script.opcodes())
    if (opcodes == SCRIPT_PUBKEYHASH_OPCODES and len(script.instructions[2].data) == 20):
        return (TX_PUBKEYHASH)
    if (opcodes == SCRIPT_PUBKEY_OPCODES and 33 <= len(script.instructions[0].data) <= 120):
        return (TX_PUBKEY)
    if (opcodes == SCRIPT_P2SH_OPCODES and len(script.instructions[1].data) == 20):
        return (TX_SCRIPTHASH)
    #TODO: add support for TX_MULTISIG 
    #see script.cpp:1188
    return None


