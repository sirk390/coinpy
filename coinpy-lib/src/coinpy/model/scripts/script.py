from coinpy.model.scripts.opcodes import OP_CHECKSIG, OP_DUP, OP_EQUALVERIFY,\
    OP_HASH160, OP_PUSHDATA, OP_CHECKSIGVERIFY, OP_CHECKMULTISIG,\
    OP_CHECKMULTISIGVERIFY, OP_CODESEPARATOR, OP_16
from coinpy.tools.hex import hexstr
from coinpy.model.scripts.opcodes_info import is_pushdata

class RawScript(object):
    """Script representation used when a script cannot be decoded.
    
       For example in PUSHDATA instructions with missing data.
    """
    def __init__(self, data):
        self.data = data
    def __str__(self):
        return ("RawScript:" + hexstr(self.data))

    
class Script(object):
    #STANDARD_TX = [OP_PUBKEY, OP_CHECKSIG]
    STANDARD_ADDRESS_TX = [OP_DUP, OP_HASH160, OP_PUSHDATA, OP_EQUALVERIFY, OP_CHECKSIG]
    
    
    def __init__(self, instructions, serialized_size=None):
        self.instructions = instructions
        self.serialized_size = serialized_size
        if len([i for i in self.instructions if (i.opcode > OP_16)]) > 201:
            raise Exception(">201 opcodes")
            
    def opcodes(self):
        return ([i.opcode for i in self.instructions])

    def last_codeseparator_index(self):
        codesep_idx = None
        for idx, instr in enumerate(self.instructions):
            if instr.opcode == OP_CODESEPARATOR:
                codesep_idx = idx
        return codesep_idx
    
    def signed_part(self):
        codesep_idx = self.last_codeseparator_index()
        if (codesep_idx != None):
            return Script(self.instructions[codesep_idx+1:])
        return Script(self.instructions)
    
    #script.cpp:Solver:962
    def is_standard_address_tx(self):
        return (self.opcodes() == self.STANDARD_ADDRESS_TX)

    def is_standard(self):
        return (self.is_standard_address_tx())
    
    def is_pushonly(self):
        return (all(i.is_pushdata() for i in self.instructions))

    def sig_op_count(self):
        count = 0
        for i in self.instructions:
            if (i.opcode == OP_CHECKSIG or i.opcode == OP_CHECKSIGVERIFY):
                count += 1
        return count
    
    def multisig_op_count(self):
        count = 0
        for i in self.instructions:
            if (i.opcode == OP_CHECKMULTISIG or i.opcode == OP_CHECKMULTISIGVERIFY):
                count += 1
        return count    

    def __str__(self):
        #if (self.is_standard_address_tx()):
        #    return ("script:STD(%s...)" % ("".join("%02x" % ord(c) for c in self.instructions[2].data[:4])))
        #if (self.is_pushonly()):
        #    return ("script:PUSHONLY(%s...)" % ("".join((",".join( "%02x" % ord(c) for c in i.data[:4])) for i in self.instructions)))
        return (",".join(str(i) for i in self.instructions))
 
    def __eq__(self, other):
        return all([i1 == i2 for i1, i2 in zip(self.instructions, other.instructions)])
    def __ne__(self, other):
        return any([i1 != i2 for i1, i2 in zip(self.instructions, other.instructions)])
    def __hash__(self):
        if len(self.instructions):
            #return the hash of the first pushdata instruction
            for instr in self.instructions:
                if is_pushdata(instr.opcode):
                    return hash(self.instruction[0])
            #or the hash of the first instruction if there is no pushdata
            return hash(self.instruction[0])
        return 0
    
if __name__ == '__main__':
    script1 = [118, 169, 20, 118, 205, 62, 179, 249, 40, 71, 171, 78, 57, 98, 179, 1, 106, 201, 223, 31, 19, 69, 100, 136, 172]
    script2 = [118, 169, 20, 138, 48, 61, 201, 194, 97, 46, 215, 75, 169, 205, 170, 115, 16, 131, 249, 21, 163, 168, 31, 136, 172]
    script3 = [118, 169, 20, 119, 86, 10, 254, 237, 20, 146, 83, 39, 165, 5, 42, 61, 22, 60, 182, 248, 248, 105, 157, 136, 172]
    script4 = [118, 169, 20, 70, 10, 115, 2, 86, 83, 11, 75, 157, 174, 174, 244, 34, 70, 243, 73, 154, 90, 85, 235, 136, 172]
    from coinpy.model.scripts.serialize import ScriptSerializer
    print ScriptSerializer().deserialize("".join(chr(c) for c in script1))
    print ScriptSerializer().deserialize("".join(chr(c) for c in script2))
    print ScriptSerializer().deserialize("".join(chr(c) for c in script3))
    print ScriptSerializer().deserialize("".join(chr(c) for c in script4))
    print  ScriptSerializer().deserialize("".join(chr(c) for c in script4)).is_standard()
    