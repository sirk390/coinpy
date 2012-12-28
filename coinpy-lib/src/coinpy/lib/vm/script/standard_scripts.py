""" Standard Scripts:

* SCRIPT_PUBKEY
    * scriptPubKey: OP_PUSHDATA, OP_CHECKSIG
    * scriptSig: OP_PUSHDATA
    
* SCRIPT_PUBKEY_HASH
    * scriptPubKey: OP_DUP, OP_HASH160, OP_PUSHDATA, OP_EQUALVERIFY, OP_CHECKSIG
    * scriptSig: OP_PUSHDATA OP_PUSHDATA
    
* SCRIPT_PAY2SH
    * scriptPubKey: OP_HASH160, OP_PUSHDATA, OP_EQUAL
    * scriptSig: OP_PUSHDATA OP_PUSHDATA, ...(push_only)
    
"""
from coinpy.model.scripts.opcodes import OP_CHECKSIG, OP_PUSHDATA, OP_DUP,\
    OP_EQUALVERIFY, OP_HASH160, OP_EQUAL, OP_CHECKMULTISIG
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.script import Script
from coinpy.lib.vm.script.push_data import push_data_instruction,\
    push_bignum_instruction

SCRIPT_PUBKEY_OPCODES = [OP_PUSHDATA, OP_CHECKSIG]
SCRIPT_PUBKEYHASH_OPCODES = [OP_DUP, OP_HASH160, OP_PUSHDATA, OP_EQUALVERIFY, OP_CHECKSIG]
SCRIPT_P2SH_OPCODES = [OP_HASH160, OP_PUSHDATA, OP_EQUAL]


class ScriptPubkey():
    """TX_PUBKEY: Script of the form 'OP_PUSHDATA(33-120), OP_CHECKSIG'"""
    def __init__(self, pubkey):
        self.pubkey = pubkey
        
    def get_script(self):
        return Script([push_data_instruction(data=self.pubkey),
                       Instruction(OP_CHECKSIG)])
    @staticmethod
    def from_script(self, script):
        if not self.match(script):
            raise Exception("Not a SCRIPT_PUBKEY script")
        return ScriptPubkey(script.instructions[0].data)
    
    @staticmethod
    def match(script):
        return (len(script.instructions) == 2 and
                script.instructions[0].ispushdata() and
                33 <= len(script.instructions[0].data) <= 120 and
                script.instructions[1].opcode == OP_CHECKSIG)

class ScriptPubkeyHash():
    """TX_PUBKEYHASH: Script of the form 'OP_DUP, OP_HASH160, OP_PUSHDATA(20), OP_EQUALVERIFY, OP_CHECKSIG'"""
    def __init__(self, pubkey_hash):
        self.pubkey_hash = pubkey_hash
        
    def get_script(self):
        return Script([Instruction(OP_DUP),
                       Instruction(OP_HASH160),
                       push_data_instruction(data=self.pubkey_hash),
                       Instruction(OP_EQUALVERIFY),
                       Instruction(OP_CHECKSIG)])
    @staticmethod
    def from_script(self, script):
        if not self.match(script):
            raise Exception("Not a SCRIPT_PUBKEY_HASH script")
        return ScriptPubkeyHash(script.instructions[2].data)
    
    @staticmethod
    def match(script):
        return (len(script.instructions) == 5 and
                script.instructions[0].opcode == OP_DUP and
                script.instructions[1].opcode == OP_HASH160 and
                script.instructions[2].ispushdata() and
                len(script.instructions[2].data) == 20 and
                script.instructions[3].opcode == OP_EQUALVERIFY and
                script.instructions[4].opcode == OP_CHECKSIG)
    
class ScriptHash():
    """TX_SCRIPTHASH: Script of the form 'OP_HASH160, OP_PUSHDATA(?), OP_EQUAL'"""
    def __init__(self, hash):
        self.hash = hash
        
    def get_script(self):
        return Script([Instruction(OP_HASH160),
                       push_data_instruction(data=self.hash),
                       Instruction(OP_EQUAL)])
    @staticmethod
    def from_script(script):
        if not ScriptHash.match(script):
            raise Exception("Not a TX_SCRIPT_HASH script")
        return ScriptPubkeyHash(script.instructions[1].data)
    
    @staticmethod
    def match(script):
        #Note: P2SH only contains OP_20 (not OP_PUSHDATA1,2, or 4)
        return (len(script.instructions) == 3 and
                script.instructions[0].opcode == OP_HASH160 and
                script.instructions[1].opcode == 20 and
                script.instructions[2].opcode == OP_EQUAL)
    
class ScriptMutlisig():
    """Script of the form 'OP_PUSHDATA(m), [OP_PUSHDATA... (n times)], OP_PUSHDATA(n), OP_CHECKMULTISIG'
    
    Attributes:
        public_keys (list of str) : public keys.
        m (int) : number of required signatures.
    """
    def __init__(self, public_keys, m):
        self.public_keys = public_keys
        self.m = m
        
    def get_script(self):
        return Script([push_bignum_instruction(data=self.m)] +
                      [push_data_instruction(pubkey) for pubkey in self.public_keys] + 
                      [push_bignum_instruction(data=len(self.public_keys))] +
                      Instruction(OP_CHECKMULTISIG))
    @staticmethod
    def from_script(self, script):
        if not self.match(script):
            raise Exception("Not a TX_SCRIPT_HASH script")
        #TODO
        return ScriptMutlisig()
    
    @staticmethod
    def match(script):
        #TODO
        return (False)

STANDARD_SCRIPTS = [ScriptPubkey, ScriptPubkeyHash, ScriptMutlisig]
STANDARD_SCRIPTS_OR_P2SH = STANDARD_SCRIPTS + [ScriptHash]

def is_standard(script):
    for s in STANDARD_SCRIPTS:
        if s.match(script):
            return True
    return False 

def is_standard_or_p2sh(script):
    for s in STANDARD_SCRIPTS_OR_P2SH:
        if s.match(script):
            return True
    return False 

# SCRIPT_PUBKEY
def make_script_pubkey(pubkey):
    instructions = [push_data_instruction(data=pubkey),
                    Instruction(OP_CHECKSIG)]
    return Script(instructions)

def make_script_pubkey_sig(sig):
    return Script([push_data_instruction(data=sig)])  

def tx_pubkey_get_pubkey(script):
    """Return the pubkey of a TX_PUBKEY"""
    return script.instructions[0].data

# SCRIPT_PUBKEY_HASH
def make_script_pubkeyhash(pubkey_hash):
    #Improve to take a BitcoinAddress?
    instructions = [Instruction(OP_DUP),
                    Instruction(OP_HASH160),
                    push_data_instruction(data=pubkey_hash),
                    Instruction(OP_EQUALVERIFY),
                    Instruction(OP_CHECKSIG)]
    return Script(instructions)

def make_script_pubkeyhash_sig(pubkey, sig):
    return Script([push_data_instruction(data=sig),
                   push_data_instruction(data=pubkey)])  

def tx_pubkeyhash_get_address(script):
    """Return the hash160 address of a TX_PUBKEYHASH"""
    return script.instructions[2].data

