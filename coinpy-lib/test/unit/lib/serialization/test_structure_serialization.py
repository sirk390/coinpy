import unittest
from coinpy.lib.serialization.structures.s11n_block import BlockSerializer
from coinpy.model.protocol.structures.blockheader import BlockHeader
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.tools.hex import hexstr, decodehexstr
from coinpy.model.protocol.structures.block import Block
from coinpy.model.protocol.structures.outpoint import Outpoint
from coinpy.model.scripts.script import Script
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.protocol.structures.tx_out import TxOut
from coinpy.model.protocol.structures.tx_in import TxIn
from coinpy.model.scripts.opcodes import OP_DUP, OP_HASH160, OP_PUSHDATA,\
    OP_CHECKSIG, OP_EQUALVERIFY
from coinpy.model.protocol.structures.tx import Tx
from coinpy.model.constants.bitcoin import COIN
from coinpy.lib.serialization.structures.s11n_blocklocator import BlockLocatorSerializer
from coinpy.model.protocol.structures.blocklocator import BlockLocator
from coinpy.model.protocol.structures.invitem import Invitem, INV_BLOCK, INV_TX
from coinpy.lib.serialization.structures.s11n_invitem import InvitemSerializer

class TestStructureSerialization(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_block_serialize(self):
        blockheader = BlockHeader(version=1,
                                  hash_prev=Uint256.from_hexstr("000000000fec081581146e8b16b275bfa52150ac4174a246cdf62694671ea7a3"),
                                  hash_merkle=Uint256.from_hexstr("0d9da162550fc45b1aaa00e933b23b3cbc7f37a9b2d2070d61235eaec11a926a"), 
                                  time=1301129903, 
                                  bits=470809215, 
                                  nonce=1280448751)
        tx1 = Tx(version=1, 
                 in_list=[TxIn(previous_output=Outpoint.null(), 
                               script=Script([Instruction(4, decodehexstr("7ffa0f1c")),
                                               Instruction(1, decodehexstr("4e"))]), 
                               sequence=TxIn.NSEQUENCE_FINAL )],
                 out_list=[TxOut(value=5002000000, 
                                 script=Script([Instruction(65, decodehexstr("049cc3cae30927c40598032044b9e9e25f4739b0d7ade62803f5e9cf075debc817e6d29f42c70d0a1beb1c904eaaa50ef885b011f9fbaa16ef288a7ad193e11567")), 
                                                Instruction(OP_CHECKSIG)]))],
                 locktime=0)
        tx2 = Tx(version=1, 
                 in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("17c5cb687ba453ab65e12cdc0d8721c70ab4678665eb200c50cb9f1e3207090e"), index=0), 
                               script=Script([Instruction(72, decodehexstr("3045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c01")),
                                              Instruction(65, decodehexstr("04b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3e"))]), 
                               sequence=TxIn.NSEQUENCE_FINAL )],
                 out_list=[TxOut(value=24990000000, 
                                 script=Script([Instruction(OP_DUP),
                                                Instruction(OP_HASH160),
                                                Instruction(20, decodehexstr("4d8b17fbce571614be89df4bd872de892a479844")), 
                                                Instruction(OP_EQUALVERIFY),
                                                Instruction(OP_CHECKSIG)])),
                           TxOut(value=5000000000, 
                                 script=Script([Instruction(OP_DUP),
                                                Instruction(OP_HASH160),
                                                Instruction(20, decodehexstr("fadad27c40adbe230f5e3c04d44a292975084831")), 
                                                Instruction(OP_EQUALVERIFY),
                                                Instruction(OP_CHECKSIG)]))],
                 locktime=0)
        blk = Block(blockheader, [tx1, tx2])
        data = BlockSerializer().serialize(blk)
        self.assertEquals(data, decodehexstr("01000000a3a71e679426f6cd46a27441ac5021a5bf75b2168b6e14811508ec0f000000006a921ac1ae5e23610d07d2b2a9377fbc3c3bb233e900aa1a5bc40f5562a19d0dafaa8d4d7ffa0f1cef18524c0201000000010000000000000000000000000000000000000000000000000000000000000000ffffffff07047ffa0f1c014effffffff018076242a010000004341049cc3cae30927c40598032044b9e9e25f4739b0d7ade62803f5e9cf075debc817e6d29f42c70d0a1beb1c904eaaa50ef885b011f9fbaa16ef288a7ad193e11567ac0000000001000000010e0907321e9fcb500c20eb658667b40ac721870ddc2ce165ab53a47b68cbc517000000008b483045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c014104b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3effffffff02802385d1050000001976a9144d8b17fbce571614be89df4bd872de892a47984488ac00f2052a010000001976a914fadad27c40adbe230f5e3c04d44a29297508483188ac00000000"))

    def test_block_deserialize(self):
        blk, _ = BlockSerializer().deserialize(decodehexstr("01000000a3a71e679426f6cd46a27441ac5021a5bf75b2168b6e14811508ec0f000000006a921ac1ae5e23610d07d2b2a9377fbc3c3bb233e900aa1a5bc40f5562a19d0dafaa8d4d7ffa0f1cef18524c0201000000010000000000000000000000000000000000000000000000000000000000000000ffffffff07047ffa0f1c014effffffff018076242a010000004341049cc3cae30927c40598032044b9e9e25f4739b0d7ade62803f5e9cf075debc817e6d29f42c70d0a1beb1c904eaaa50ef885b011f9fbaa16ef288a7ad193e11567ac0000000001000000010e0907321e9fcb500c20eb658667b40ac721870ddc2ce165ab53a47b68cbc517000000008b483045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c014104b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3effffffff02802385d1050000001976a9144d8b17fbce571614be89df4bd872de892a47984488ac00f2052a010000001976a914fadad27c40adbe230f5e3c04d44a29297508483188ac00000000"))
        
        blockheader = BlockHeader(version=1,
                                  hash_prev=Uint256.from_hexstr("000000000fec081581146e8b16b275bfa52150ac4174a246cdf62694671ea7a3"),
                                  hash_merkle=Uint256.from_hexstr("0d9da162550fc45b1aaa00e933b23b3cbc7f37a9b2d2070d61235eaec11a926a"), 
                                  time=1301129903, 
                                  bits=470809215, 
                                  nonce=1280448751)
        tx1 = Tx(version=1, 
                 in_list=[TxIn(previous_output=Outpoint.null(), 
                               script=Script([Instruction(4, decodehexstr("7ffa0f1c")),
                                               Instruction(1, decodehexstr("4e"))]), 
                               sequence=TxIn.NSEQUENCE_FINAL )],
                 out_list=[TxOut(value=5002000000, 
                                 script=Script([Instruction(65, decodehexstr("049cc3cae30927c40598032044b9e9e25f4739b0d7ade62803f5e9cf075debc817e6d29f42c70d0a1beb1c904eaaa50ef885b011f9fbaa16ef288a7ad193e11567")), 
                                                Instruction(OP_CHECKSIG)]))],
                 locktime=0)
        tx2 = Tx(version=1, 
                 in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("17c5cb687ba453ab65e12cdc0d8721c70ab4678665eb200c50cb9f1e3207090e"), index=0), 
                               script=Script([Instruction(72, decodehexstr("3045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c01")),
                                              Instruction(65, decodehexstr("04b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3e"))]), 
                               sequence=TxIn.NSEQUENCE_FINAL )],
                 out_list=[TxOut(value=24990000000, 
                                 script=Script([Instruction(OP_DUP),
                                                Instruction(OP_HASH160),
                                                Instruction(20, decodehexstr("4d8b17fbce571614be89df4bd872de892a479844")), 
                                                Instruction(OP_EQUALVERIFY),
                                                Instruction(OP_CHECKSIG)])),
                           TxOut(value=5000000000, 
                                 script=Script([Instruction(OP_DUP),
                                                Instruction(OP_HASH160),
                                                Instruction(20, decodehexstr("fadad27c40adbe230f5e3c04d44a292975084831")), 
                                                Instruction(OP_EQUALVERIFY),
                                                Instruction(OP_CHECKSIG)]))],
                 locktime=0)
        self.assertEquals(blk, Block(blockheader, [tx1, tx2]))

    def test_blockheader_serialize(self):
        h = BlockHeader(version=1, 
                        hash_prev=Uint256.from_hexstr("1e4baab89f3a3251818c31bc87f6a33b4a5a88ef76673e2cc77ab2127b7afded"), #hash_prev
                        hash_merkle=Uint256.from_hexstr("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"), #merkle
                        time=1237006505,
                        bits=486605799, 
                        nonce=2083236893) 
        self.assertEquals(hexstr(BlockheaderSerializer().serialize(h)), "01000000edfd7a7b12b27ac72c3e6776ef885a4a3ba3f687bc318c8151323a9fb8aa4b1e3ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4aa938bb49e703011d1dac2b7c") 
        

    def test_blockheader_deserialize(self):
        h, cursor = BlockheaderSerializer().deserialize(decodehexstr("01000000edfd7a7b12b27ac72c3e6776ef885a4a3ba3f687bc318c8151323a9fb8aa4b1e3ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4aa938bb49e703011d1dac2b7c"))
        self.assertEquals(h,
                          BlockHeader(version=1, 
                                      hash_prev=Uint256.from_hexstr("1e4baab89f3a3251818c31bc87f6a33b4a5a88ef76673e2cc77ab2127b7afded"), #hash_prev
                                      hash_merkle=Uint256.from_hexstr("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"), #merkle
                                      time=1237006505, 
                                      bits=486605799,
                                      nonce=2083236893)) 
        
    def test_blocklocator_serialize(self):
        loc = BlockLocator(version=1,
                           blockhashlist=[Uint256.from_hexstr("0000000002ae3d2db6477a04ad37bdcbc111c06050effb0ceab2376016e129a3"),
                                          Uint256.from_hexstr("00000000074150f20eb97a8aec12a8dc7f93ddebb3b2df0d8022a60213b4bd70"),
                                          Uint256.from_hexstr("0000000025345b019b2ee713a995dfc3250d88232e2253f95ec42c4bb2528039"),
                                          Uint256.from_hexstr("000000007dbb8690940f40293832c46b90a20bfef681b52979115fb1049a7366"),
                                          Uint256.from_hexstr("00000007199508e34a9ff81e6ec0c477a4cccff2a4767a8eee39c11db367b008")])
        self.assertEquals(hexstr(BlockLocatorSerializer().serialize(loc)), 
                          "0100000005a329e1166037b2ea0cfbef5060c011c1cbbd37ad047a47b62d3dae020000000070bdb41302a622800ddfb2b3ebdd937fdca812ec8a7ab90ef250410700000000398052b24b2cc45ef953222e23880d25c3df95a913e72e9b015b34250000000066739a04b15f117929b581f6fe0ba2906bc4323829400f949086bb7d0000000008b067b31dc139ee8e7a76a4f2cfcca477c4c06e1ef89f4ae308951907000000")

    def test_blocklocator_deserialize(self):
        loc, cursor = BlockLocatorSerializer().deserialize(decodehexstr("0100000005a329e1166037b2ea0cfbef5060c011c1cbbd37ad047a47b62d3dae020000000070bdb41302a622800ddfb2b3ebdd937fdca812ec8a7ab90ef250410700000000398052b24b2cc45ef953222e23880d25c3df95a913e72e9b015b34250000000066739a04b15f117929b581f6fe0ba2906bc4323829400f949086bb7d0000000008b067b31dc139ee8e7a76a4f2cfcca477c4c06e1ef89f4ae308951907000000"))
        self.assertEquals(loc, BlockLocator(version=1,
                                            blockhashlist=[Uint256.from_hexstr("0000000002ae3d2db6477a04ad37bdcbc111c06050effb0ceab2376016e129a3"),
                                                           Uint256.from_hexstr("00000000074150f20eb97a8aec12a8dc7f93ddebb3b2df0d8022a60213b4bd70"),
                                                           Uint256.from_hexstr("0000000025345b019b2ee713a995dfc3250d88232e2253f95ec42c4bb2528039"),
                                                           Uint256.from_hexstr("000000007dbb8690940f40293832c46b90a20bfef681b52979115fb1049a7366"),
                                                           Uint256.from_hexstr("00000007199508e34a9ff81e6ec0c477a4cccff2a4767a8eee39c11db367b008")]))

    def test_invitem_serialize(self):
        blockitem = Invitem(INV_BLOCK, Uint256.from_hexstr("00000007199508e34a9ff81e6ec0c477a4cccff2a4767a8eee39c11db367b008"))
        txitem = Invitem(INV_TX, Uint256.from_hexstr("84eb3cf3a391a0a0b70e05a3a54d8385f7dcb3809aaf274d392622205b27f288"))
        self.assertEquals(hexstr(InvitemSerializer().serialize(blockitem)), 
                          "0200000008b067b31dc139ee8e7a76a4f2cfcca477c4c06e1ef89f4ae308951907000000")
        self.assertEquals(hexstr(InvitemSerializer().serialize(txitem)), 
                          "0100000088f2275b202226394d27af9a80b3dcf785834da5a3050eb7a0a091a3f33ceb84")

    def test_invitem_deserialize(self):
        blockitem, cursor = InvitemSerializer().deserialize(decodehexstr("0200000008b067b31dc139ee8e7a76a4f2cfcca477c4c06e1ef89f4ae308951907000000"))
        txitem, cursor = InvitemSerializer().deserialize(decodehexstr("0100000088f2275b202226394d27af9a80b3dcf785834da5a3050eb7a0a091a3f33ceb84"))
        self.assertEquals(blockitem, Invitem(INV_BLOCK, Uint256.from_hexstr("00000007199508e34a9ff81e6ec0c477a4cccff2a4767a8eee39c11db367b008")))
        self.assertEquals(txitem, Invitem(INV_TX, Uint256.from_hexstr("84eb3cf3a391a0a0b70e05a3a54d8385f7dcb3809aaf274d392622205b27f288")))

    """
    def test_serialize(self):
        obj = Invitem(INV_BLOCK, Uint256.from_hexstr("00000007199508e34a9ff81e6ec0c477a4cccff2a4767a8eee39c11db367b008"))
        self.assertEquals(hexstr(InvitemSerializer().serialize(obj)), 
                          "")

    def test_deserialize(self):
        obj, cursor = InvitemSerializer().deserialize(decodehexstr(""))
        self.assertEquals(obj, )
                                            
    """                             

    def test_ipaddrfield_serialisation(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
    
