from coinpy.model.scripts.opcodes import OP_PUSHDATA
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY
from coinpy.model.scripts.opcodes_info import is_pushdata
from coinpy.lib.script.script_pubkeyhash import SCRIPT_PUBKEYHASH_OPCODES
from coinpy.lib.script.script_pubkey import SCRIPT_PUBKEY_OPCODES



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
    #TODO: add support for TX_MULTISIG and TX_SCRIPTHASH
    #see script.cpp:1188
    return None

""" 
    Returns the hash160 address of a TX_PUBKEYHASH
"""
def tx_pubkeyhash_get_address(script):
    return script.instructions[2].data

""" 
    Returns the pubkey of a TX_PUBKEY
"""
def tx_pubkey_get_pubkey(script):
    return script.instructions[0].data

