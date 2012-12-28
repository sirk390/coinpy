import unittest
import json
import os
import re
from coinpy.model.scripts.script import RawScript
from coinpy.lib.vm.script.push_data import push_bignum_instruction,\
    push_data_instruction
from coinpy.tools.hex import decodehexstr
from coinpy.model.scripts.opcodes_info import OPCODES_BY_NAME
from coinpy.model.scripts.instruction import Instruction
from coinpy.lib.vm.vm import TxValidationVM
from coinpy.lib.serialization.scripts.serialize import InstructionSerializer,\
    ScriptSerializer
from coinpy.model.scripts.opcodes import OP_1

def parse_instruction(inst_str):
    serializer = InstructionSerializer()
    if re.match("^-?[0-9]+$", inst_str):
        i = int(inst_str)
        if (i == -1 or (1 <=  i <= 16)):
            return serializer.serialize(Instruction(i + OP_1 - 1))
        else:
            return serializer.serialize(push_bignum_instruction(i))
        return serializer.serialize(push_bignum_instruction(i))
    if re.match("^'[^']*'$", inst_str):
        return serializer.serialize(push_data_instruction(str(inst_str[1:-1])))
    elif re.match("^0x[0-9A-Fa-f]+$", inst_str):
        return decodehexstr(inst_str[2:])
    elif inst_str in OPCODES_BY_NAME:
        return serializer.serialize(Instruction(OPCODES_BY_NAME[inst_str]))
    elif ("OP_" + inst_str) in OPCODES_BY_NAME:
        return serializer.serialize(Instruction(OPCODES_BY_NAME["OP_" + inst_str]))
    raise Exception("Wrong format: '" + inst_str + "'")
    
def parse_script(json_script):
    serializer = ScriptSerializer()
    if json_script != "":
        instr = [parse_instruction(elm) for elm in re.split("[ \n\t]", json_script)]
        script_bin = "".join(instr)
    else:
        script_bin = ""
    result = serializer.deserialize(script_bin)
    return result

def test_script(vm, claim_script_str, unspent_script_str):
    try:
        claim_script = parse_script(claim_script_str)
        unspent_script = parse_script(unspent_script_str)
    except Exception as e:
        return (False, str(e))
    if isinstance(claim_script, RawScript) or isinstance(unspent_script, RawScript):
        return (False, "RawScript")
    valid, reason = vm.validate(None, None, unspent_script, claim_script)
    return valid, reason

class TestScriptsJson(unittest.TestCase):
    def setUp(self):
        self.vm = TxValidationVM()
        self.current_dir = os.path.dirname(__file__)
        
    def test_scripts_valid(self):
        with open(os.path.join(self.current_dir, "data","script_valid.json")) as fp:
            testcase_list = json.load(fp)
        for testcase in testcase_list:
            claim_script = parse_script(testcase[0])
            unspent_script  = parse_script(testcase[1])
            valid, reason = self.vm.validate(None, None, unspent_script, claim_script)
            if not valid:
                raise Exception(reason)
                
    def test_scripts_invalid(self):
        with open(os.path.join(self.current_dir, "data","script_invalid.json")) as fp:
            testcase_list = json.load(fp)
        for testcase in testcase_list:
            valid, reason = test_script(self.vm, testcase[0], testcase[1])
            if valid:
                raise Exception("Script is valid %s" % (testcase))
    
if __name__ == '__main__':
    unittest.main()
    
