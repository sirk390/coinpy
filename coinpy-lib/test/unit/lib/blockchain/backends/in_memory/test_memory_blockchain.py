import unittest
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.tools.log.basic_logger import stdout_logger
from coinpy.lib.blockchain.in_memory.database import InMemoryBlockchainDatabase
from unit.lib.blockchain.backends.in_memory.data.blockchain_5blocks_unitnet import blockchain_5blocks_unitnet
from coinpy.model.blockchain.blockchain_database import TransactionNotFound,\
    BlockNotFound
from coinpy.model.protocol.structures.tx import Tx
from coinpy.model.protocol.structures.block import Block
from coinpy.model.protocol.structures.blockheader import BlockHeader

class TestInMemoryBlockchainDatabase(unittest.TestCase):
    def setUp(self):
        self.log = stdout_logger()
        self.database1 = InMemoryBlockchainDatabase(blockchain_5blocks_unitnet)

    def test_contains_transaction(self):
        self.assertTrue(self.database1.contains_transaction(Uint256.from_hexstr("a87f530f2174f6c12945831e731a6fc99f699f1539cf14f36357b66d267b75a8")))
        self.assertFalse(self.database1.contains_transaction(Uint256.from_hexstr("07c17eafb870acf0fece060b814ff71fd36a7df0f0a3a7e359c2c61b3b34c3e1")))

    def test_transaction_handle(self):
        with self.assertRaises(TransactionNotFound):
            self.database1.get_transaction_handle(Uint256.from_hexstr("07c17eafb870acf0fece060b814ff71fd36a7df0f0a3a7e359c2c61b3b34c3e1"))
        handle1 = self.database1.get_transaction_handle(Uint256.from_hexstr("cebbc8d7d3550ca6df92eba4f41b93dc55f35b8199bb14dc3d0a95f9bd0e2dbd"))
        assert isinstance(handle1.get_transaction(), Tx)
        self.assertEquals(str(handle1.get_block_hash()), "001f9c93fece90e2e1f729bb9c2b04ba59432592f8ebdc7d117146c74f7c833a")
        self.assertEquals(handle1.output_count(), 7)
        self.assertEquals(handle1.is_output_spent(0), False)
        self.assertEquals(handle1.is_output_spent(2), True)
        self.assertEquals(str(handle1.get_spending_transaction_hash(2)), 
                          "53bb1c14b4c6156d7352ee471fb7697736f4696accf5392e0f1830e38143f667")
        handle1.mark_unspent(2)
        self.assertEquals(handle1.is_output_spent(2), False)
        handle1.mark_spent(0, Uint256.from_hexstr("13bb1c14b4c6156d7352ee471fb7697736f4696accf5392e0f1830e38143f667"))
        self.assertEquals(handle1.is_output_spent(2), False)
        self.assertEquals(handle1.is_output_spent(0), True)
        self.assertEquals(str(handle1.get_spending_transaction_hash(0)), 
                          "13bb1c14b4c6156d7352ee471fb7697736f4696accf5392e0f1830e38143f667")
        
    def test_get_block_handle(self):
        with self.assertRaises(BlockNotFound):
            self.database1.get_block_handle(Uint256.from_hexstr("041f9c93fece90e2e1f729bb9c2b04ba59432592f8ebdc7d117146c74f7c833a"))
        handle1 = self.database1.get_block_handle(Uint256.from_hexstr("001f9c93fece90e2e1f729bb9c2b04ba59432592f8ebdc7d117146c74f7c833a"))
        self.assertEquals(handle1.get_height(), 4)
        self.assertEquals(handle1.get_hash(), Uint256.from_hexstr("001f9c93fece90e2e1f729bb9c2b04ba59432592f8ebdc7d117146c74f7c833a"))
        assert isinstance(handle1.get_block(), Block)
        assert isinstance(handle1.get_blockheader(), BlockHeader)

    def test_pop_append_block(self):
        self.assertTrue(self.database1.contains_transaction(Uint256.from_hexstr("53bb1c14b4c6156d7352ee471fb7697736f4696accf5392e0f1830e38143f667")))
        block = self.database1.pop_block()
        self.assertFalse(self.database1.contains_transaction(Uint256.from_hexstr("53bb1c14b4c6156d7352ee471fb7697736f4696accf5392e0f1830e38143f667")))
        self.database1.append_block(block)
        self.assertTrue(self.database1.contains_transaction(Uint256.from_hexstr("53bb1c14b4c6156d7352ee471fb7697736f4696accf5392e0f1830e38143f667")))

    def test_next_in_mainchain(self):
        self.assertEquals(self.database1.get_next_in_mainchain(Uint256.from_hexstr("003ee3cf880906caa5662f10d4b4fb1c86c1853230dee8a7b8a62f434c73da5f")),
                          Uint256.from_hexstr("000cdbffc59b95168c34e5f1853075376308c05c53a1a53425d7f1ca9cab7073"))
        self.assertIs(self.database1.get_next_in_mainchain(Uint256.from_hexstr("002afdfc8ed8111fa00c98bb7b94c34e02a52c57ba971a5fd29935d68fa1060b")),
                      None)

    def test_next_get_genesis(self):
        self.assertEquals(self.database1.get_genesis_hash(),
                          Uint256.from_hexstr("003ee3cf880906caa5662f10d4b4fb1c86c1853230dee8a7b8a62f434c73da5f"))

    def test_next_get_best_hash(self):
        self.assertEquals(self.database1.get_best_hash(),
                          Uint256.from_hexstr("002afdfc8ed8111fa00c98bb7b94c34e02a52c57ba971a5fd29935d68fa1060b"))
    
if __name__ == '__main__':
    unittest.main()

