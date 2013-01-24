import unittest
from coinpy.lib.transactions.address import BitcoinAddress,\
    InvalidBitcoinAddress
from coinpy.model.protocol.runmode import MAIN, TESTNET
from coinpy.tools.hex import hexstr, decodehexstr
from coinpy.model.address_version import PUBKEY_ADDRESS_MAIN,\
    PUBKEY_ADDRESS_TEST, AddressVersion, SCRIPT_ADDRESS_TEST,\
    SCRIPT_ADDRESS_MAIN
from coinpy.model.protocol.structures.tx import Tx
from coinpy.model.protocol.structures.outpoint import Outpoint
from coinpy.model.protocol.structures.tx_in import TxIn
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.model.scripts.script import Script
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.opcodes import OP_CHECKSIG, OP_DUP, OP_EQUALVERIFY,\
    OP_HASH160
from coinpy.model.protocol.structures.tx_out import TxOut
from coinpy.lib.transactions.sign_transaction import sign_transaction_input,\
    sign_transaction
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY
from int.exp.dump_tx import dump_script
from coinpy.lib.vm.vm import TxValidationVM
from coinpy.tools.ssl.ecdsa import KEY
from coinpy.tools.bitcoin.hash160 import hash160
from coinpy.lib.serialization.scripts.serialize import ScriptSerializer

class TestSignTransaction(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_sign_transaction_input(self):
        tx = Tx(version=1, 
                in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("d2a42ebcb98b598ddcb6d430ce9061dba76804a97f7c1413dd3faef744f909a8"),index=0), 
                   script=Script(instructions=[]), 
                   sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("2be8e319be1d15c1ba54708bdd7969b638e7e6fa2154819136e363ea6d33664a"),index=1), 
                   script=Script(instructions=[]), 
                   sequence=4294967295)], 
                out_list=[TxOut(value=3315075843, 
                    script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("297c5a2ee31a1ab721115722d83f8654ca21d5df")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])),TxOut(value=2971972133, 
                    script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("7d5feab86e31e8fc99d8e735d56226de9043e5fc")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])),TxOut(value=1046301823, 
                    script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("fd91232a2fa0c389fa0188efde26c8a6165f4c50")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)]))], 
                locktime=0)

        outscript0 = Script(instructions=[Instruction(33,  decodehexstr("03409fe679bdff9e801692c999b86d0c47b62dc02cdd10591ee70ca8056cd05023")),Instruction(OP_CHECKSIG)])
        outscript1 = Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("5fb7fdb3d1ab0f3fec90b38417cca8ab736b10c6")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])

        # Sign TX_PUBKEY 
        sign_transaction_input(tx, 
                               0,
                               outscript0,
                               TX_PUBKEY,
                               decodehexstr("f006b27418527b1c400bbc434a3f22ee57c376bd4819cfe2a1162682788ae714"))
        # Sign TX_PUBKEYHASH with hash160 of compressed public key. 
        sign_transaction_input(tx, 
                               1,
                               outscript1,
                               TX_PUBKEYHASH,
                               decodehexstr("c693115901c2840badd1e404706a4866a90d3afa16a542c1a3d0de9aad0875fe"))

        vm = TxValidationVM()
        valid, reason = vm.validate(tx, 0, outscript0, tx.in_list[0].script)
        if not valid:
            raise Exception(reason)
        valid, reason = vm.validate(tx, 1, outscript1, tx.in_list[1].script)
        if not valid:
            raise Exception(reason)

    def test_sign_transaction(self):
        tx = Tx(version=1, 
                in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("d2a42ebcb98b598ddcb6d430ce9061dba76804a97f7c1413dd3faef744f909a8"),index=0), 
                   script=Script(instructions=[]), 
                   sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("2be8e319be1d15c1ba54708bdd7969b638e7e6fa2154819136e363ea6d33664a"),index=1), 
                   script=Script(instructions=[]), 
                   sequence=4294967295)], 
                out_list=[TxOut(value=3315075843, 
                    script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("297c5a2ee31a1ab721115722d83f8654ca21d5df")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])),TxOut(value=2971972133, 
                    script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("7d5feab86e31e8fc99d8e735d56226de9043e5fc")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])),TxOut(value=1046301823, 
                    script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("fd91232a2fa0c389fa0188efde26c8a6165f4c50")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)]))], 
                locktime=0)

        outscript0 = Script(instructions=[Instruction(33,  decodehexstr("03409fe679bdff9e801692c999b86d0c47b62dc02cdd10591ee70ca8056cd05023")),Instruction(OP_CHECKSIG)])
        outscript1 = Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("5fb7fdb3d1ab0f3fec90b38417cca8ab736b10c6")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])

        # Sign TX_PUBKEY 
        sign_transaction(tx, 
                         [TxOut(None, outscript0), TxOut(None, outscript1)],
                         [decodehexstr("f006b27418527b1c400bbc434a3f22ee57c376bd4819cfe2a1162682788ae714"),
                          decodehexstr("c693115901c2840badd1e404706a4866a90d3afa16a542c1a3d0de9aad0875fe")])

        vm = TxValidationVM()
        valid, reason = vm.validate(tx, 0, outscript0, tx.in_list[0].script)
        if not valid:
            raise Exception(reason)
        valid, reason = vm.validate(tx, 1, outscript1, tx.in_list[1].script)
        if not valid:
            raise Exception(reason)

""" real example (pubkey is compressed before hashing):

TX 1 of block 48212 of TESTNET3.
 hash: 2d3fa964202b70092e9d2ae2e38a3414caae646f87e7e1531ab38d6e1d5519fc
 
 Tx(version=1, 
        in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("1080a78b53205c40a524b02db95b0245c532d8878495ec46572ea95cd978cfad"),index=1), 
           script=Script(instructions=[Instruction(72,  decodehexstr("30450220447da1ff4fe20116b9f9d6e6688dfe5c621be0e7c5d2a6545c46266934ab8c91022100abd865dba878eb696606dd70b07b34ab23f9768f977dfbd2f0f51c5aaaa1094801")),Instruction(33,  decodehexstr("02a949412fa46c44746c2f94a42fff448e2be131bc7c905d8d632615b51fb383fc"))]), 
           sequence=4294967295)], 
        out_list=[TxOut(value=3999950000, 
            script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("556825ce66be9bde37fcb4c04d3f3ccba3aa859c")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])),TxOut(value=1000000000, 
            script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("7abf72ef083647cd2cb792c9435ce854bee00aee")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)]))], 
        locktime=0)
        
public: 02a949412fa46c44746c2f94a42fff448e2be131bc7c905d8d632615b51fb383fc
private: abc62a5ae1694fcd55a984634ef92cdac867300fc54f33380f31da74bc248e5c
"""
if __name__ == '__main__':
    unittest.main()
    
