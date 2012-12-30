import unittest
from coinpy.tools.hex import decodehexstr
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.opcodes import OP_CHECKSIG, OP_EQUALVERIFY, OP_HASH160,\
    OP_DUP
from coinpy.model.scripts.script import Script
from coinpy.lib.vm.script.standard_scripts import ScriptPubkeyHash

class TestPubkeyHash(unittest.TestCase):
    def setUp(self):
        self.script1 = Script([Instruction(OP_DUP),
                               Instruction(OP_HASH160),
                               Instruction(20,  decodehexstr("342e5d1f2eb9c6e99fda90c85ca05aa36616644c")),
                               Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])
        
    def test_pubkeyhash_match(self):
        assert ScriptPubkeyHash.match(self.script1)

    def test_pubkeyhash_from_script(self):
        self.assertEquals(ScriptPubkeyHash.from_script(self.script1),
                          ScriptPubkeyHash(decodehexstr("342e5d1f2eb9c6e99fda90c85ca05aa36616644c")))
    
    def test_pubkeyhash_get_script(self):
        self.assertEquals(ScriptPubkeyHash(decodehexstr("342e5d1f2eb9c6e99fda90c85ca05aa36616644c")).get_script(),
                          self.script1)

if __name__ == '__main__':
    unittest.main()