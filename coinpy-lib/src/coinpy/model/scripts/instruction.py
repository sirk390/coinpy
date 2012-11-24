from coinpy.model.scripts.opcodes import OP_PUSHDATA1_75_MIN, OP_PUSHDATA1_75_MAX, OP_PUSHDATA1, OP_PUSHDATA4, OP_PUSHDATA2
from coinpy.model.scripts.opcodes_info import OPCODE_NAMES, is_pushdata
from coinpy.tools.hex import hexstr

# Note: Instructions are modelized using specific opcodes for each different PUSH_DATA variant.
# This is required as one could still put an OP_PUSHDATA4 instruction in the blockchain with less than 0xffff characters
# We always need to have serialize(deserialize(SCRIPTDATA) == SCRIPTDATA for signatures.
class Instruction():
    def __init__(self, opcode, data=None):
        self.opcode = opcode            #value defined in opcodes.py
        self.data = data                #optional (bytestring for pushdata)
        
    #def ispush(self):
    #    return (OP_0 <= self.opcode <= OP_16)

    def __pushdata__str__(self):
        datastr = hexstr(self.data)
        if OP_PUSHDATA1_75_MIN <= self.opcode <= OP_PUSHDATA1_75_MAX:
            return ("OP_PUSHDATA(%d):%s" % (self.opcode, datastr))
        if  self.opcode == OP_PUSHDATA1:
            return ("OP_PUSHDATA1:%s" % (datastr))
        if  self.opcode == OP_PUSHDATA2:
            return ("OP_PUSHDATA2:%s" % (datastr))
        if  self.opcode == OP_PUSHDATA4:
            return ("OP_PUSHDATA4:%s" % (datastr))
        
    def __str__(self):
        if is_pushdata(self.opcode):
            return self.__pushdata__str__()
        if (self.opcode in OPCODE_NAMES):
            return OPCODE_NAMES[self.opcode]
        return ("UNKNOWN(%d)" % self.opcode)
    
    def __eq__(self, other):
        return (self.opcode == other.opcode and self.data == other.data)
    def __ne__(self, other):
        return (self.opcode != other.opcode or self.data != other.data)
    def __hash__(self):
        if is_pushdata(self.opcode):
            return hash(self.data)
        return self.opcode
    