import unittest
from coinpy.tools.hex import decodehexstr
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.opcodes import OP_CHECKMULTISIG, OP_2, OP_3
from coinpy.model.scripts.script import Script
from coinpy.lib.vm.script.standard_scripts import ScriptPubkey, ScriptMutlisig

class TestMultiSig(unittest.TestCase):
    def setUp(self):
        self.script1 = Script([Instruction(OP_2),
                               Instruction(33, decodehexstr("02547b223d58eb5da7c7690748f70a3bab1509cb7578faac9032399f0b6bce31d6")),
                               Instruction(33, decodehexstr("c47a2dbbfb38f02205a3a72a37c68a8c068fe71a1351516f0f1fe7dd3c7afce38f")),
                               Instruction(33, decodehexstr("9f1de01000000fd45010047304402200983ab9c46fd1194e541c683828bbb92ce9")),
                               Instruction(OP_3),
                               Instruction(OP_CHECKMULTISIG)])
        
    def test_pubkeyhash_match(self):
        assert ScriptMutlisig.match(self.script1)

    def test_pubkeyhash_from_script(self):
        self.assertEquals(ScriptMutlisig.from_script(self.script1),
                          ScriptMutlisig(2,
                                         [decodehexstr("02547b223d58eb5da7c7690748f70a3bab1509cb7578faac9032399f0b6bce31d6"),
                                          decodehexstr("c47a2dbbfb38f02205a3a72a37c68a8c068fe71a1351516f0f1fe7dd3c7afce38f"),
                                          decodehexstr("9f1de01000000fd45010047304402200983ab9c46fd1194e541c683828bbb92ce9")]))
    
    def test_pubkeyhash_get_script(self):
        self.assertEquals(ScriptMutlisig(2,
                                         [decodehexstr("02547b223d58eb5da7c7690748f70a3bab1509cb7578faac9032399f0b6bce31d6"),
                                          decodehexstr("c47a2dbbfb38f02205a3a72a37c68a8c068fe71a1351516f0f1fe7dd3c7afce38f"),
                                          decodehexstr("9f1de01000000fd45010047304402200983ab9c46fd1194e541c683828bbb92ce9")]).get_script(),
                          self.script1)

if __name__ == '__main__':
    unittest.main()