# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.lib.vm.opcode_impl.opcode_functions import OPCODE_FUNCTIONS
from coinpy.lib.serialization.messages.s11n_tx import tx_encoder
from coinpy.tools.hex import decodehexstr
import traceback

class TxValidationVM():
    def __init__(self):
        self.stack = []
        self.altstack = []
        self.checksig_data = None

    def validate(self, transaction, inputindex, unspent_script, claim_script):
        try:
            self.set_checksig_data(transaction, inputindex, unspent_script)
            self.eval(claim_script)
            self.eval(unspent_script)
            return (len(self.stack) == 1) and (self.stack[0] == True)
        except:
            traceback.print_exc()
            return (False)

    def eval(self, script):
        for i in script.instructions:
            OPCODE_FUNCTIONS[i.opcode](self, i)

    def set_checksig_data(self, transaction, inputindex, unspent_script):
        self.checksig_data = (transaction, inputindex, unspent_script)  
    
    """
        ['OP_PUSHDATA(73:30460221...]', 'OP_PUSHDATA(65:048791c5...]']
        ['OP_DUP', 'OP_HASH160', 'OP_PUSHDATA(20:76cd3eb3...]', 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    """

if __name__ == '__main__':
    script_in = [73, 48, 70, 2, 33, 0, 188, 221, 205, 147, 181, 60, 249, 233, 89, 25, 224, 231, 189, 215, 220, 191, 14, 134, 226, 144, 44, 104, 222, 114, 183, 105, 188, 254, 100, 104, 201, 6, 2, 33, 0, 254, 79, 216, 238, 184, 16, 161, 169, 207, 84, 125, 153, 254, 113, 118, 138, 213, 121, 191, 241, 96, 53, 230, 134, 144, 161, 236, 164, 171, 154, 185, 20, 1, 65, 4, 135, 145, 197, 22, 141, 185, 55, 52, 230, 127, 0, 161, 37, 96, 89, 76, 201, 148, 92, 112, 134, 43, 85, 56, 39, 116, 187, 189, 33, 94, 55, 62, 198, 244, 141, 149, 104, 149, 173, 203, 119, 180, 57, 213, 161, 186, 248, 44, 10, 231, 179, 146, 77, 86, 251, 199, 167, 244, 243, 180, 31, 101, 116, 95]
    script_out = [118, 169, 20, 118, 205, 62, 179, 249, 40, 71, 171, 78, 57, 98, 179, 1, 106, 201, 223, 31, 19, 69, 100, 136, 172]
    from coinpy.model.scripts.serialize import ScriptSerializer
    s1 = ScriptSerializer().deserialize("".join(chr(c) for c in script_in))
    s2 = ScriptSerializer().deserialize("".join(chr(c) for c in script_out))
    print [str(i) for i in s1.instructions]
    print [str(i) for i in s2.instructions]
    
    txdata = "0100000003219f0a306fa848cc4d028d90fc2c566acb5f594d01f2aacb4c09ce362903ee82000000008b483045022100a63ae2cc3e8ffc169d6e5169c6d6b2af3446efe268adebede497c6fca4b6f67f02205d838c285af5161032db5474bfdec4e69e2e0f66b8ef5458b5b18281eeabbc2b014104ab35c8334824f753e7502948d03aef75d7c7a724a7f2363256d4055c5d06aae9c0412fe01aabd5069f2c60477372bbee3b6aa1c9e2bbc95b280c9a28ed4c16a4ffffffff8bac88cc30abb176a17c5d91f66d2aafd5443817edef88bad43d161b4e3432ce000000008a47304402206a6e84e844210abdb42e71864d64942dc1e8d37ba6e85853596b9bf56bc3eda7022032c5ade4b0bfe019581756ccf063d72a1a3a13c343177443a97e3392406e1ef5014104a4586fe5c49cb2e4510caaaf45e01d31bcfeddaa9bb043b6deb56fd6ab23d7187796d82c45c3a55824b6e32dd45e56182ffb570299569086a24f4ba94419c26dffffffffc93eaf1a0b51a96e8d6facd60be8924b6d7618d2baca23abfe23d97178c17541000000008b48304502204dc83602eac8b2382ebd851f7bda02fae6a4f9b32d2fda7ac1dd977a417718c4022100d4fded75970fad1e51a392f735663fa7e3f794b2cdfe1c9708cc977677a0620a0141049171f7af90d0d6e8ef89a19844a9f685e96606065590d6e17c6ba2f1383fa679fd00a4c41274abfa3234fb7b7747ea167299c963ea3ee4b991c93507a456a08dffffffff0240ac2700000000001976a914119017a544834d557fe126f9411cdad07c99a7b888ac801d2c04000000001976a914129d3ea19d92a9620cf5d17c25a4f0288bd2951688ac00000000"
    tx, cursor = tx_encoder().decode(decodehexstr(txdata))
    unspent_script_hex = "76a914db1cab70296702a214726b5eb0b7da5dac99b46388ac"
    unspent_script = ScriptSerializer().deserialize( decodehexstr(unspent_script_hex))
    inputindex = 0
    
    vm = TxValidationVM()
    isvalid = vm.validate(tx, inputindex, unspent_script, tx.in_list[inputindex].script)
    print isvalid

