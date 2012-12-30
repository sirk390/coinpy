import unittest
from coinpy.tools.hex import decodehexstr
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer
from coinpy.lib.serialization.scripts.serialize import ScriptSerializer
from coinpy.lib.vm.vm import TxValidationVM
from coinpy.lib.transactions.hash_tx import hash_tx

class TestScriptExamples(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_pubkey(self):
        # tx 1 of block 383 on testnet 3 (2 PUBKEY inputs)
        # tx: 43cd28c3b56543298ee264e3c01ef2dd8189276bd0c1cf6b86269018c710ce28
        tx, _ =  TxSerializer().deserialize(decodehexstr("01000000028e3430573cfde2f3e1eece8aefe661dd841bcb665d35832415bab4f75267852200000000494830450221009cca8fb1c4a34982c4e9a59fd15856404c02085f926043cfc6664924a5b9e36d02205811f85b395c43492164b8b33867d745211d8c7ffdcd1b288e56f74dbdaed15b01ffffffffe3abf5981a1bd6457ec0cdcab76cc2a176dc0d7e16f6d3781aebc684f13cc4fd00000000484730440220387bbcee99e370ea2115eaccfd8c48eb380653303b66c6946e0903fb0bbc6f8602202b2ef048519d45525413f64b727a1d85ff2cf7d91ab4607308224b4c30d5846801ffffffff0240f1f23a000000001976a9142203ca59edf66969757e6cc9238b1b36f4dc35b888acc0f218190200000017a9149eb21980dc9d413d8eac27314938b9da920ee53e8700000000"))
        outscript1 = ScriptSerializer().deserialize(decodehexstr("2102547b223d58eb5da7c7690748f70a3bab1509cb7578faac9032399f0b6bce31d6ac"))
        outscript2 = ScriptSerializer().deserialize(decodehexstr("2103fcc9ce029ad74af9fecacce68bcc775cc6efcb000a0b8cc2b3aacad4850bc4b0ac"))

        vm = TxValidationVM()
        valid, reason = vm.validate(tx, 0, outscript1, tx.in_list[0].script)
        assert valid, reason
        valid, reason = vm.validate(tx, 1, outscript2, tx.in_list[1].script)
        assert valid, reason

    def test_validate_pubkeyhash(self):
        # tx 5 of block 506 on testnet 3 (2 PUBKEYHASH inputs)
        # tx: e79d5732b9914a511c0ad002c930271aa843ae64ed0abf54bff2869596c04a59
        tx, _ =  TxSerializer().deserialize(decodehexstr("010000000202f630b1641c6988224295e4299c14d176fb4446d0f62a682efc6adbd049de77000000006b483045022100cb6600d5be418a84e3f5c7e7ece2836de358ccbdb26fc1a4e4c262c0db117cf2022058cceb2e810ed5c7c3a4d47c0fec4e09e2672490645767579893ce89c0c50087012102de4a86f3c045cfa9460dbe867ebedab96df36aa662800e2f1d8645374f0d10a4ffffffff3b7de9fe37b52af96fd4f7134df83c91358c40687430812f8e29841085363a87000000006a47304402205b26712719619a2d8510d888a2e2cd65ceba00b104f95d1bc46da04f71814a7d022046af82c57609914a855de48ea0036a09fdbccc7996c79406a6eef383242f994301210321b73cc97e906155d3c5bf65e5a2ee75f6792c97916f1c6ceda59777baa0dcc5ffffffff02b3c40e00000000001976a9146d9ad15ddc32b1f96d9f496a4a8a89a77ab88fa388ac87200f00000000001976a914431143b62421c12c1149f1252ae1e181547b0e5d88ac00000000"))
        outscript1 = ScriptSerializer().deserialize(decodehexstr("76a9141b05d1cc4b3158519041814fdac587326422865b88ac"))
        outscript2 = ScriptSerializer().deserialize(decodehexstr("76a914b5d23a56ad5657163698a6817420f17b47cf3c4588ac"))
        vm = TxValidationVM()
        valid, reason = vm.validate(tx, 0, outscript1, tx.in_list[0].script)
        assert valid, reason
        vm = TxValidationVM()
        valid, reason = vm.validate(tx, 1, outscript2, tx.in_list[1].script)
        assert valid, reason

    def test_validate_scripthash_multisig(self):
        # tx 1 of block 504 on testnet 3, 2 TX_SCRIPTHASH inputs, 2 PUBKEYHASH outputs
        # SCRIPTHASH of 1-of-2 and 2-of-3 multisig transactions
        # tx: 1915695f1de19d9a2e1fb1bd9c5e2f816022ec41a58e9f298396c8a4586a8c5e
        tx, _ =  TxSerializer().deserialize(decodehexstr("0100000002c142078d793bb5b4aadba6009e2b142872b1ed3a7f0f7336ebe0e38180d8d682010000009200483045022100d6868ef86978ffad889a312be2991cbfe2c2d27b40fed038dc65da83565f5b0f02205f7019af9b75a5e9ba9c394f6ce883fa72e8e0951cf2ca5011af5888026663f3014751210341d8a934cfca197c7acaa358a1c39b3317a3e6d80b808ad367278ddb6661d16f210220108eea941a69b20d320e9a82c4bc5f096edb7e7c74638810227594a8033c1d52aeffffffff3f2dc10288706fe1c3116bec01dc2a259bfc2802b60d9b13787195fa8205f0cf01000000b400473044022066952731f8c5663fd61b2cbc33361e79e27a8c0937c32b42cc2dd125215b98bb02202c90d8022337c868c1f00ab59a9cd833cad2522de4b703264e9b4e271d11cd12014c6951210220108eea941a69b20d320e9a82c4bc5f096edb7e7c74638810227594a8033c1d210386380591c6fe54fe67d54e809d38d2db63886c1d228beb744abc9327bee392882102c4c0101075ed2d413dd328841c87f7a39ff5a75d793decab1da9fb1128082c3b53aeffffffff02c11e1400000000001976a914724192ac202d067d06635dc043b84abdad14de0088ac2b540400000000001976a914342e5d1f2eb9c6e99fda90c85ca05aa36616644c88ac00000000"))
        outscript1 = ScriptSerializer().deserialize(decodehexstr("a914d9f26cca817fa116dc76e1be7a17067eb843625087"))
        outscript2 = ScriptSerializer().deserialize(decodehexstr("a9145fc04212c7fb1103d99dd7ff454797a281ef92f587"))

        vm = TxValidationVM()
        valid, reason = vm.validate(tx, 0, outscript1, tx.in_list[0].script)
        assert valid, reason
        valid, reason = vm.validate(tx, 1, outscript2, tx.in_list[1].script)
        assert valid, reason


if __name__ == '__main__':
    unittest.main()