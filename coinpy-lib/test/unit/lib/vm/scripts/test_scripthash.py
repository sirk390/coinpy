import unittest
from coinpy.tools.hex import decodehexstr
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.opcodes import OP_CHECKSIG
from coinpy.model.scripts.script import Script
from coinpy.lib.vm.script.standard_scripts import ScriptPubkey

class TestPubkey(unittest.TestCase):
    def setUp(self):
        self.script1 = Script([Instruction(33, decodehexstr("02547b223d58eb5da7c7690748f70a3bab1509cb7578faac9032399f0b6bce31d6")),
                               Instruction(OP_CHECKSIG)])
        
    def test_pubkeyhash_match(self):
        assert ScriptPubkey.match(self.script1)

    def test_pubkeyhash_from_script(self):
        self.assertEquals(ScriptPubkey.from_script(self.script1),
                          ScriptPubkey(decodehexstr("02547b223d58eb5da7c7690748f70a3bab1509cb7578faac9032399f0b6bce31d6")))
    
    def test_pubkeyhash_get_script(self):
        self.assertEquals(ScriptPubkey(decodehexstr("02547b223d58eb5da7c7690748f70a3bab1509cb7578faac9032399f0b6bce31d6")).get_script(),
                          self.script1)

if __name__ == '__main__':
    unittest.main()