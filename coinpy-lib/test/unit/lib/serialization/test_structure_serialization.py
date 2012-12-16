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
    OP_CHECKSIG, OP_EQUALVERIFY, OP_EQUAL
from coinpy.model.protocol.structures.tx import Tx
from coinpy.model.constants.bitcoin import COIN
from coinpy.lib.serialization.structures.s11n_blocklocator import BlockLocatorSerializer
from coinpy.model.protocol.structures.blocklocator import BlockLocator
from coinpy.model.protocol.structures.invitem import Invitem, INV_BLOCK, INV_TX
from coinpy.lib.serialization.structures.s11n_invitem import InvitemSerializer
from coinpy.lib.serialization.structures.s11n_ipaddrfield import IPAddrSerializer
from coinpy.model.protocol.structures.netaddr import Netaddr
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK, SERVICES_NONE
from coinpy.lib.serialization.structures.s11n_netaddrfield import NetAddrSerializer
from coinpy.lib.serialization.structures.s11n_outpoint import OutpointSerializer
from coinpy.model.protocol.structures.timenetaddr import Timenetaddr
from coinpy.lib.serialization.structures.s11n_timenetaddr import TimenetaddrSerializer
from coinpy.lib.serialization.structures.s11n_tx_in import TxinSerializer
from coinpy.lib.serialization.structures.s11n_tx_out import TxoutSerializer
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.structures.s11n_varstr_script import VarstrScriptSerializer
from coinpy.lib.serialization.structures.s11n_varstr import VarstrSerializer
from coinpy.model.protocol.structures.merkle_tx import MerkleTx
from coinpy.lib.serialization.structures.s11n_merkle_tx import MerkleTxSerializer

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
        blockitem, _ = InvitemSerializer().deserialize(decodehexstr("0200000008b067b31dc139ee8e7a76a4f2cfcca477c4c06e1ef89f4ae308951907000000"))
        txitem, _ = InvitemSerializer().deserialize(decodehexstr("0100000088f2275b202226394d27af9a80b3dcf785834da5a3050eb7a0a091a3f33ceb84"))
        self.assertEquals(blockitem, Invitem(INV_BLOCK, Uint256.from_hexstr("00000007199508e34a9ff81e6ec0c477a4cccff2a4767a8eee39c11db367b008")))
        self.assertEquals(txitem, Invitem(INV_TX, Uint256.from_hexstr("84eb3cf3a391a0a0b70e05a3a54d8385f7dcb3809aaf274d392622205b27f288")))
    
    def test_ipaddr_serialize(self):
        self.assertEquals(hexstr(IPAddrSerializer().serialize("178.3.5.12")), 
                          "00000000000000000000ffffb203050c")

    def test_ipaddr_deserialize(self):
        ip, _ = IPAddrSerializer().deserialize(decodehexstr("00000000000000000000ffffb203050c"))
        self.assertEquals(ip, "178.3.5.12")
                      
    def test_merkletx_serialize(self):
        # This is tx 37 of block 429 on testnet3
        merkle_tx = MerkleTx(
                 Tx(version=1, 
                    in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("88c844570a227fe89d82e4e20d41576b95df8aa790a799bf7114dbed83b788b0"),index=0), 
                       script=Script(instructions=[Instruction(72,  decodehexstr("3045022100813a4dfdfda02946bf9fddc59ffd0b8d2feaa618518a3015fd5e65dd88a0d4480220137b25ea7531e103405bfe1617cb92f524e88c86e66a79c1e3c62558d019528201")),Instruction(33,  decodehexstr("03cf163e38520a7b390305528eca2fa1c620f0da225a044017fd92b30067875dc8"))]), 
                       sequence=4294967295)], 
                    out_list=[TxOut(value=4899704976, 
                         script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("10170e3f7c3b0c93d2e07e90e307d3fb21811702")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])),TxOut(value=887733, 
                        script=Script(instructions=[Instruction(OP_HASH160),Instruction(20,  decodehexstr("184cd0a38ac3b1357d07179553788375a9e8a3b8")),Instruction(OP_EQUAL)]))], 
                    locktime=0),
                 blockhash=Uint256.from_hexstr("00000000e080223655db52d2c35a37f6aa17a3f2efefa6794fd9831374cff09f"),
                 merkle_branch=[Uint256.from_hexstr("88c844570a227fe89d82e4e20d41576b95df8aa790a799bf7114dbed83b788b0"), 
                                Uint256.from_hexstr("225dd6a6857be59dbf2d72d4d5cca1325053dd66a9c3a35a16c51de04a1b0d03"), 
                                Uint256.from_hexstr("74f79002e7c2cbbf40581aa56d8037cb32844d34ae049629a757b6ff709a10fa"),
                                Uint256.from_hexstr("02099d8b6bf46c3f87ccc922dec8c18a9dc420e17ebc672030145bd8ee33ab34"), 
                                Uint256.from_hexstr("15b202c47b1ad2638c4ea260611839be7cdf15e13e6de50861f41e46a5e9f8cf"), 
                                Uint256.from_hexstr("007e2166afda37ce696e971ac530a7cc22e183b37acf57c79cb0ee21a9de2179"), 
                                Uint256.from_hexstr("a7d06d9452a65fae2662ae63c9b450ba4ce22dfab76d22624a95d97d294421d4")],
                 nindex=37)
        self.assertEquals(hexstr(MerkleTxSerializer().serialize(merkle_tx)), 
                          "0100000001b088b783eddb1471bf99a790a78adf956b57410de2e4829de87f220a5744c888000000006b483045022100813a4dfdfda02946bf9fddc59ffd0b8d2feaa618518a3015fd5e65dd88a0d4480220137b25ea7531e103405bfe1617cb92f524e88c86e66a79c1e3c62558d0195282012103cf163e38520a7b390305528eca2fa1c620f0da225a044017fd92b30067875dc8ffffffff0290900b24010000001976a91410170e3f7c3b0c93d2e07e90e307d3fb2181170288acb58b0d000000000017a914184cd0a38ac3b1357d07179553788375a9e8a3b887000000009ff0cf741383d94f79a6efeff2a317aaf6375ac3d252db55362280e00000000007b088b783eddb1471bf99a790a78adf956b57410de2e4829de87f220a5744c888030d1b4ae01dc5165aa3c3a966dd535032a1ccd5d4722dbf9de57b85a6d65d22fa109a70ffb657a7299604ae344d8432cb37806da51a5840bfcbc2e70290f77434ab33eed85b14302067bc7ee120c49d8ac1c8de22c9cc873f6cf46b8b9d0902cff8e9a5461ef46108e56d3ee115df7cbe39186160a24e8c63d21a7bc402b2157921dea921eeb09cc757cf7ab383e122cca730c51a976e69ce37daaf66217e00d42144297dd9954a62226db7fa2de24cba50b4c963ae6226ae5fa652946dd0a725000000")                    

    def test_merkletx_deserialize(self):
        # This is tx 37 of block 429 on testnet3
        merkle_tx_data = "0100000001b088b783eddb1471bf99a790a78adf956b57410de2e4829de87f220a5744c888000000006b483045022100813a4dfdfda02946bf9fddc59ffd0b8d2feaa618518a3015fd5e65dd88a0d4480220137b25ea7531e103405bfe1617cb92f524e88c86e66a79c1e3c62558d0195282012103cf163e38520a7b390305528eca2fa1c620f0da225a044017fd92b30067875dc8ffffffff0290900b24010000001976a91410170e3f7c3b0c93d2e07e90e307d3fb2181170288acb58b0d000000000017a914184cd0a38ac3b1357d07179553788375a9e8a3b887000000009ff0cf741383d94f79a6efeff2a317aaf6375ac3d252db55362280e00000000007b088b783eddb1471bf99a790a78adf956b57410de2e4829de87f220a5744c888030d1b4ae01dc5165aa3c3a966dd535032a1ccd5d4722dbf9de57b85a6d65d22fa109a70ffb657a7299604ae344d8432cb37806da51a5840bfcbc2e70290f77434ab33eed85b14302067bc7ee120c49d8ac1c8de22c9cc873f6cf46b8b9d0902cff8e9a5461ef46108e56d3ee115df7cbe39186160a24e8c63d21a7bc402b2157921dea921eeb09cc757cf7ab383e122cca730c51a976e69ce37daaf66217e00d42144297dd9954a62226db7fa2de24cba50b4c963ae6226ae5fa652946dd0a725000000"
        expected_merkle_tx = MerkleTx(
                                 Tx(version=1, 
                                    in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("88c844570a227fe89d82e4e20d41576b95df8aa790a799bf7114dbed83b788b0"),index=0), 
                                       script=Script(instructions=[Instruction(72,  decodehexstr("3045022100813a4dfdfda02946bf9fddc59ffd0b8d2feaa618518a3015fd5e65dd88a0d4480220137b25ea7531e103405bfe1617cb92f524e88c86e66a79c1e3c62558d019528201")),Instruction(33,  decodehexstr("03cf163e38520a7b390305528eca2fa1c620f0da225a044017fd92b30067875dc8"))]), 
                                       sequence=4294967295)], 
                                    out_list=[TxOut(value=4899704976, 
                                         script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("10170e3f7c3b0c93d2e07e90e307d3fb21811702")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])),TxOut(value=887733, 
                                         script=Script(instructions=[Instruction(OP_HASH160),Instruction(20,  decodehexstr("184cd0a38ac3b1357d07179553788375a9e8a3b8")),Instruction(OP_EQUAL)]))], 
                                    locktime=0),
                                 blockhash=Uint256.from_hexstr("00000000e080223655db52d2c35a37f6aa17a3f2efefa6794fd9831374cff09f"),
                                 merkle_branch=[Uint256.from_hexstr("88c844570a227fe89d82e4e20d41576b95df8aa790a799bf7114dbed83b788b0"), 
                                                Uint256.from_hexstr("225dd6a6857be59dbf2d72d4d5cca1325053dd66a9c3a35a16c51de04a1b0d03"), 
                                                Uint256.from_hexstr("74f79002e7c2cbbf40581aa56d8037cb32844d34ae049629a757b6ff709a10fa"),
                                                Uint256.from_hexstr("02099d8b6bf46c3f87ccc922dec8c18a9dc420e17ebc672030145bd8ee33ab34"), 
                                                Uint256.from_hexstr("15b202c47b1ad2638c4ea260611839be7cdf15e13e6de50861f41e46a5e9f8cf"), 
                                                Uint256.from_hexstr("007e2166afda37ce696e971ac530a7cc22e183b37acf57c79cb0ee21a9de2179"), 
                                                Uint256.from_hexstr("a7d06d9452a65fae2662ae63c9b450ba4ce22dfab76d22624a95d97d294421d4")],
                                 nindex=37)
        
        self.assertEquals(MerkleTxSerializer().deserialize(decodehexstr(merkle_tx_data))[0], 
                          expected_merkle_tx)                    

    def test_netaddr_serialize(self):
        self.assertEquals(hexstr(NetAddrSerializer().serialize(Netaddr(SERVICES_NODE_NETWORK, "178.3.5.12", 2007))), 
                          "010000000000000000000000000000000000ffffb203050c07d7")

    def test_netaddr_deserialize(self):
        netaddr, _ = NetAddrSerializer().deserialize(decodehexstr("000000000000000000000000000000000000ffffb203050c07d7"))
        self.assertEquals(netaddr, Netaddr(SERVICES_NONE, "178.3.5.12", 2007))


    def test_outpoint_serialize(self):
        self.assertEquals(hexstr(OutpointSerializer().serialize(Outpoint(hash=Uint256.from_hexstr("17c5cb687ba453ab65e12cdc0d8721c70ab4678665eb200c50cb9f1e3207090e"), index=0))), 
                          "0e0907321e9fcb500c20eb658667b40ac721870ddc2ce165ab53a47b68cbc51700000000")

    def test_outpoint_deserialize(self):
        outpoint, _ = OutpointSerializer().deserialize(decodehexstr("0e0907321e9fcb500c20eb658667b40ac721870ddc2ce165ab53a47b68cbc51700000000"))
        self.assertEquals(outpoint, Outpoint(hash=Uint256.from_hexstr("17c5cb687ba453ab65e12cdc0d8721c70ab4678665eb200c50cb9f1e3207090e"), index=0))



    def test_timenetaddr_serialize(self):
        self.assertEquals(hexstr(TimenetaddrSerializer().serialize(Timenetaddr(timestamp=1355658677, netaddr= Netaddr(SERVICES_NONE, "178.3.5.12", 2007)))), 
                          "b5b5cd50000000000000000000000000000000000000ffffb203050c07d7")

    def test_timenetaddr_deserialize(self):
        timenetaddr, _ = TimenetaddrSerializer().deserialize(decodehexstr("b5b5cd50000000000000000000000000000000000000ffffb203050c07d7"))
        self.assertEquals(timenetaddr, Timenetaddr(timestamp=1355658677, netaddr= Netaddr(SERVICES_NONE, "178.3.5.12", 2007)))

    def test_txin_serialize(self):
        txin = TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("17c5cb687ba453ab65e12cdc0d8721c70ab4678665eb200c50cb9f1e3207090e"), index=0), 
                               script=Script([Instruction(72, decodehexstr("3045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c01")),
                                              Instruction(65, decodehexstr("04b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3e"))]), 
                               sequence=TxIn.NSEQUENCE_FINAL)
        self.assertEquals(hexstr(TxinSerializer().serialize(txin)), 
                          "0e0907321e9fcb500c20eb658667b40ac721870ddc2ce165ab53a47b68cbc517000000008b483045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c014104b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3effffffff")

    def test_txin_deserialize(self):
        txin, _ = TxinSerializer().deserialize(decodehexstr("0e0907321e9fcb500c20eb658667b40ac721870ddc2ce165ab53a47b68cbc517000000008b483045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c014104b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3effffffff"))
        self.assertEquals(txin, TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("17c5cb687ba453ab65e12cdc0d8721c70ab4678665eb200c50cb9f1e3207090e"), index=0), 
                               script=Script([Instruction(72, decodehexstr("3045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c01")),
                                              Instruction(65, decodehexstr("04b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3e"))]), 
                               sequence=TxIn.NSEQUENCE_FINAL))

    def test_txout_serialize(self):
        txout = TxOut(value=24990000000, 
                      script=Script([Instruction(OP_DUP),
                                     Instruction(OP_HASH160),
                                     Instruction(20, decodehexstr("4d8b17fbce571614be89df4bd872de892a479844")), 
                                     Instruction(OP_EQUALVERIFY),
                                     Instruction(OP_CHECKSIG)]))
        self.assertEquals(hexstr(TxoutSerializer().serialize(txout)), 
                          "802385d1050000001976a9144d8b17fbce571614be89df4bd872de892a47984488ac")

    def test_txout_deserialize(self):
        txout, _ = TxoutSerializer().deserialize(decodehexstr("802385d1050000001976a9144d8b17fbce571614be89df4bd872de892a47984488ac"))
        self.assertEquals(txout, TxOut(value=24990000000, 
                                       script=Script([Instruction(OP_DUP),
                                                      Instruction(OP_HASH160),
                                                      Instruction(20, decodehexstr("4d8b17fbce571614be89df4bd872de892a479844")), 
                                                      Instruction(OP_EQUALVERIFY),
                                                      Instruction(OP_CHECKSIG)])))
        
    def test_tx_serialize(self):
        tx = Tx(version=1, 
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
        self.assertEquals(hexstr(TxSerializer().serialize(tx)), "01000000010e0907321e9fcb500c20eb658667b40ac721870ddc2ce165ab53a47b68cbc517000000008b483045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c014104b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3effffffff02802385d1050000001976a9144d8b17fbce571614be89df4bd872de892a47984488ac00f2052a010000001976a914fadad27c40adbe230f5e3c04d44a29297508483188ac00000000")
                

    def test_tx_deserialize(self):
        tx, _ = TxSerializer().deserialize(decodehexstr("01000000010e0907321e9fcb500c20eb658667b40ac721870ddc2ce165ab53a47b68cbc517000000008b483045022100ab2dc8932ca1d26f4cdac1feae09020a60ccc4d17b14e5fc5b21f3ab8c3a9cee022040a7208c172d19a19902280d66201c7fe2c3d8b2df7e23cc4e5b70fd52ecba2c014104b77dd1f3a21cb3d067a7e76982a609d7310f8692f5d61346f3225323c425604a0c12862755335c49e392673106adfc5dfdee1e4d367f10353e8911fac687db3effffffff02802385d1050000001976a9144d8b17fbce571614be89df4bd872de892a47984488ac00f2052a010000001976a914fadad27c40adbe230f5e3c04d44a29297508483188ac00000000"))
        tx_expected = Tx(version=1, 
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
        self.assertEquals(tx, tx_expected)

    def test_uint256_serialize(self):
        uint256 = Uint256.from_hexstr("0d9da162550fc45b1aaa00e933b23b3cbc7f37a9b2d2070d61235eaec11a926a")
        self.assertEquals(hexstr(Uint256Serializer().serialize(uint256)), 
                          "6a921ac1ae5e23610d07d2b2a9377fbc3c3bb233e900aa1a5bc40f5562a19d0d")

    def test_uint256_deserialize(self):
        uint256, _ = Uint256Serializer().deserialize(decodehexstr("6a921ac1ae5e23610d07d2b2a9377fbc3c3bb233e900aa1a5bc40f5562a19d0d"))
        self.assertEquals(uint256, Uint256.from_hexstr("0d9da162550fc45b1aaa00e933b23b3cbc7f37a9b2d2070d61235eaec11a926a"))
           

    def test_varint_serialize(self):
        self.assertEquals(hexstr(VarintSerializer().serialize(5)), "05")
        self.assertEquals(hexstr(VarintSerializer().serialize(252)), "fc")
        self.assertEquals(hexstr(VarintSerializer().serialize(253)), "fdfd00")
        self.assertEquals(hexstr(VarintSerializer().serialize(65535)), "fdffff")
        self.assertEquals(hexstr(VarintSerializer().serialize(65536)), "fe00000100")
        self.assertEquals(hexstr(VarintSerializer().serialize(4294967295)), "feffffffff")
        self.assertEquals(hexstr(VarintSerializer().serialize(4294967296)), "ff0000000001000000")

    def test_varint_deserialize(self):
        self.assertEquals(VarintSerializer().deserialize(decodehexstr("05"))[0], 5)
        self.assertEquals(VarintSerializer().deserialize(decodehexstr("fc"))[0], 252)
        self.assertEquals(VarintSerializer().deserialize(decodehexstr("fdfd00"))[0], 253)
        self.assertEquals(VarintSerializer().deserialize(decodehexstr("fdffff"))[0], 65535)
        self.assertEquals(VarintSerializer().deserialize(decodehexstr("fe00000100"))[0], 65536)
        self.assertEquals(VarintSerializer().deserialize(decodehexstr("feffffffff"))[0], 4294967295)
        self.assertEquals(VarintSerializer().deserialize(decodehexstr("ff0000000001000000"))[0], 4294967296)

    def test_varstr_script_serialize(self):
        script = Script([Instruction(OP_DUP),
                         Instruction(OP_HASH160),
                         Instruction(20, decodehexstr("fadad27c40adbe230f5e3c04d44a292975084831")), 
                         Instruction(OP_EQUALVERIFY),
                         Instruction(OP_CHECKSIG)])
        self.assertEquals(hexstr(VarstrScriptSerializer().serialize(script)), 
                          "1976a914fadad27c40adbe230f5e3c04d44a29297508483188ac")

    def test_varstr_script_deserialize(self):
        script, _ = VarstrScriptSerializer().deserialize(decodehexstr("1976a914fadad27c40adbe230f5e3c04d44a29297508483188ac"))
        self.assertEquals(script, Script([Instruction(OP_DUP),
                                          Instruction(OP_HASH160),
                                          Instruction(20, decodehexstr("fadad27c40adbe230f5e3c04d44a292975084831")), 
                                          Instruction(OP_EQUALVERIFY),
                                          Instruction(OP_CHECKSIG)]))
                                            
    def test_varstr_serialize(self):
        self.assertEquals(hexstr(VarstrSerializer().serialize("hello")), 
                          "0568656c6c6f")

    def test_varstr_deserialize(self):
        str, _ = VarstrSerializer().deserialize(decodehexstr("0568656c6c6f"))
        self.assertEquals(str, "hello")
      
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
    
