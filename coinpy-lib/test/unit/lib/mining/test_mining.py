from coinpy.tools.hex import decodehexstr, hexstr
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.opcodes import OP_CHECKSIG
from coinpy.model.scripts.opcodes import OP_PUSHDATA
from coinpy.model.scripts.script import Script
from unit.mocks.time_source import MockTimeSource
from coinpy.lib.mining.mining import BitcoinMiner, BlockheaderTemplate
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.model.protocol.structures.tx_out import TxOut
import unittest
from coinpy.lib.blocks.hash_block import hash_block
from coinpy.lib.transactions.merkle_tree import compute_merkle_root
from coinpy.lib.vm.script.push_data import push_data_instruction

class TestMining(unittest.TestCase):
    def test_mine_genesis_block(self):
        """ Mine the unitnet GENESIS block """
        time_source = MockTimeSource(time=1356446436)
        miner = BitcoinMiner()
        block, template = miner.mine_block(hash_prev=Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), 
                                    block_height=0,
                                    time_source=time_source, 
                                    difficulty_bits=524287999, 
                                    transactions=[], 
                                    coinbase_txout_list=[TxOut(5000000000, Script([push_data_instruction(decodehexstr("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")),Instruction(OP_CHECKSIG)]))],
                                    coinbase_flags=["/P2SH/", "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"])
        self.assertEquals(block.blockheader.nonce, 1260)
        self.assertEquals(block.blockheader.hash_merkle, Uint256.from_hexstr("cf7ac9a3b387cf5e9fc14e03e2a5bbfc16d1ba00d2af6c96869ab4da949bd240"))
        self.assertEquals(hash_block(block), Uint256.from_hexstr("003ee3cf880906caa5662f10d4b4fb1c86c1853230dee8a7b8a62f434c73da5f"))
        
    def test_blockheader_template(self):
        """ Change nonce and extra_nonce in a blockheader_template """
        template = BlockheaderTemplate(Uint256.from_hexstr("0009d8ab497a46a0d6a2b9b302993bd26613b145695d986be50e0b6e68c5b524"), 
                                       1, # version 2 blocks see BIP-34
                                       [TxOut(5000000000, Script([Instruction(OP_PUSHDATA, decodehexstr("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")),Instruction(OP_CHECKSIG)]))], 
                                       [], 
                                       time=1356447036, 
                                       bits=524287999,
                                       nonce=0,
                                       extra_nonce=0,
                                       coinbase_flags=["/P2SH/"])
        self.assertEquals(hexstr(template.get_serialized()), "0200000024b5c5686e0b0ee56b985d6945b11366d23b9902b3b9a2d6a0467a49abd80900ad7af2ede803ff129e66775d56153a7a649721e524eecad69a437ecdc01e29343cbdd950ffff3f1f00000000")
        template.set_nonce(8)
        self.assertEquals(hexstr(template.get_serialized()), "0200000024b5c5686e0b0ee56b985d6945b11366d23b9902b3b9a2d6a0467a49abd80900ad7af2ede803ff129e66775d56153a7a649721e524eecad69a437ecdc01e29343cbdd950ffff3f1f08000000")
        template.set_nonce(492498294)
        self.assertEquals(hexstr(template.get_serialized()), "0200000024b5c5686e0b0ee56b985d6945b11366d23b9902b3b9a2d6a0467a49abd80900ad7af2ede803ff129e66775d56153a7a649721e524eecad69a437ecdc01e29343cbdd950ffff3f1f76ed5a1d")
        template.set_extra_nonce(2)
        template.set_nonce(0)
        self.assertEquals(hexstr(template.get_serialized()), "0200000024b5c5686e0b0ee56b985d6945b11366d23b9902b3b9a2d6a0467a49abd80900e1cc38b530e20307a310a57a6e2e22985ce2e292bfc73b28a723dd77f8e8f0ca3cbdd950ffff3f1f00000000")

    def test_mine_block(self):
        """ Mine a block changing both nonce and extra_nonce"""
        def nonce_changer(template):
            if template.nonce >= 20:
                template.set_extra_nonce(template.extra_nonce + 1)
                template.set_nonce(0)
            else:
                template.set_nonce(template.nonce + 1)
        time_source = MockTimeSource(time=1356446436)
        miner = BitcoinMiner()
        block, template = miner.mine_block(hash_prev=Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), 
                                           block_height=0,
                                           time_source=time_source, 
                                           difficulty_bits=524287999, 
                                           transactions=[], 
                                           coinbase_txout_list=[TxOut(5000000000, Script([Instruction(OP_PUSHDATA, decodehexstr("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")),Instruction(OP_CHECKSIG)]))],
                                           nonce_changer=nonce_changer)
        self.assertEquals(block.blockheader.nonce, 8)
        self.assertEquals(template.nonce, 8)
        self.assertEquals(template.extra_nonce, 14)
        self.assertEquals(block.blockheader.hash_merkle, Uint256.from_hexstr("ca839450c8702d6768d1803bb6d99c6d059a56240933e5bf72cb2936f6c9e211"))
        self.assertEquals(hash_block(block), Uint256.from_hexstr("003c7a06c7efe128cb3bea692e1a485f7400f3670df7986c020083e9b10e295d"))
        

if __name__ == '__main__':
    unittest.main()