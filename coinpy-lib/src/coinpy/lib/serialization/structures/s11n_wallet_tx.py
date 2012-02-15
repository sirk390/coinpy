# -*- coding:utf-8 -*-
"""
Created on 15 Feb 2012

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_merkle_tx import MerkleTxSerializer
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.wallet_tx import WalletTx
from coinpy.tools.hex import decodehexstr, hexstr
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.common import varsizelist
from coinpy.lib.serialization.structures.s11n_varstr import VarstrSerializer
from coinpy.lib.serialization.common.field import Field


class WalletTxSerializer(Serializer):
    WALLET_TX = Structure([MerkleTxSerializer(),
                               VarsizelistSerializer(VarintSerializer(), MerkleTxSerializer()),
                               VarsizelistSerializer(VarintSerializer(), Structure([ VarstrSerializer(), VarstrSerializer()])),
                               VarsizelistSerializer(VarintSerializer(), Structure([ VarstrSerializer(), VarstrSerializer()])),
                               Field("<I"),
                               Field("<I"),
                               Field("b"),
                               Field("b")])
    def get_size(self, wallet_tx):
        return (self.WALLET_TX.get_size([wallet_tx.merkle_tx,
                                         wallet_tx.merkle_tx_prev,
                                         [[k,v] for k,v in wallet_tx.map_value.iteritems()],
                                         wallet_tx.order_from,
                                         int(wallet_tx.time_received_is_tx_time),
                                         wallet_tx.time_received,
                                         int(wallet_tx.from_me),
                                         int(wallet_tx.spent)]))

    def serialize(self, wallet_tx):
        print wallet_tx.map_value.items()
        return (self.WALLET_TX.serialize([wallet_tx.merkle_tx,
                                          wallet_tx.merkle_tx_prev,
                                          sorted(wallet_tx.map_value.items()),
                                          wallet_tx.order_from,
                                          int(wallet_tx.time_received_is_tx_time),
                                          wallet_tx.time_received,
                                          int(wallet_tx.from_me),
                                          int(wallet_tx.spent)]))

    def deserialize(self, data, cursor=0):
        (merkle_tx, merkle_tx_prev, map_value, 
         order_from, time_received_is_tx_time,
         time_received, from_me, spent), cursor = self.WALLET_TX.deserialize(data, cursor)
        return (WalletTx(merkle_tx, 
                         merkle_tx_prev, 
                         dict((k,v) for k,v in map_value), 
                         order_from, 
                         bool(time_received_is_tx_time), 
                         time_received, 
                         bool(from_me), 
                         bool(spent)), cursor)


if __name__ == '__main__':
    serializer = WalletTxSerializer()
    wallet_tx_data = decodehexstr("0100000002c096e279d9e75aeae844b5fe9b1328071ac4baaa9212931c4541ac7dca7be336000000008a47304402202ba0d0971404d6e0727702cd537ce42157e616053bc28bac1a523a23d5b5a64902203e88312a1ff731df24886da6ceb7b5170ef022dad7ddb2994a6a27e1eb90ee31014104c18618795e267cfe10d4cc8decc8de52bf4ba4512e1a78bf63ed02d560ce5578b6dda9d1afaa4f8c64244cf7877a19818eb91ed25fcb2b756ac84fc2ec851bbbffffffff3e4b2ea3fd40780b0945c4ea6e67c11338fe5effdd1713cc29df8b8cb2ef6011000000008b483045022100c74e67fe9003ab821634e72774b05182110a01e11c531dba91131f43c16b62c5022024a4abc9215a55f4ff6fd560b3b92c501da2df986997994cd4d9e0347845e4f8014104dabce776b1848fcf5da5f47229b24be8f5932fd0e162fd3138bbd9f1d649fb560170f0422ba34a2018520e3e56d331008d8f0d44bddcd679508c9d902135a48cffffffff02ded41000000000001976a91489d9f2e7f4c4835c32c74e949751ca2fd904595488ac0065cd1d000000001976a914eb88fb6b92f676ff0e6a352f60e3dd9b9dbf1a7888ac000000000c8cee30c3fa3c1e041d92e24c6d61d2a239015966aabc449694030d0000000003c42abb0d1a4f101cd6db922ca5e8ce2279b04ad5e7e683fe823b40d217b45658043a4588a78f51ebe877c1e3c35a7d5b8cce9c01f5502c2e459ddb1fa6f8c6ad5600a9bbb6a055cbeff94d48d80dcea2f21f384c0d16fc363d1ac1344c7f1fac0400000000020b66726f6d6163636f756e7400057370656e74000000000000d45b314f0000")
    wallet_tx, cursor = serializer.deserialize(wallet_tx_data, 0)
    print wallet_tx
    merkle_tx_data_out = serializer.serialize(wallet_tx)
    print hexstr(merkle_tx_data_out)
