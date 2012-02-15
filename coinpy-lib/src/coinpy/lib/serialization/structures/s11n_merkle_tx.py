# -*- coding:utf-8 -*-
"""
Created on 15 Feb 2012

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.common.field import Field
from coinpy.tools.hex import decodehexstr, hexstr
from coinpy.model.protocol.structures.merkle_tx import MerkleTx


class MerkleTxSerializer(Serializer):
    MERKLE_TX = Structure([TxSerializer(), 
                           Uint256Serializer(),            
                           VarsizelistSerializer(VarintSerializer(), Uint256Serializer()),
                           Field("<I", "nindex")], "tx")

    def get_size(self, tx):
        return (self.MERKLE_TX.get_size([tx.tx, tx.blockhash, tx.merkle_branch, tx.nindex]))

    def serialize(self, tx):
        return (self.MERKLE_TX.serialize([tx.tx, tx.blockhash, tx.merkle_branch, tx.nindex]))

    def deserialize(self, data, cursor=0):
        (tx, blockhash, merkle_branch, nindex), cursor = self.MERKLE_TX.deserialize(data, cursor)
        return (MerkleTx(tx, blockhash, merkle_branch, nindex), cursor)


if __name__ == '__main__':
    serializer = MerkleTxSerializer()
    merkle_tx_data = decodehexstr("0100000001c043487b307bd97b85ac5241ffff6ce12eb3823f2538996910c995cb076bcdb7000000004a493046022100a0f0cdd2a6f03f0652202123d05cb7fa4e46f2b38c937ece3a6c98486fa6633f022100d74b8b30e70313bf76f89a114806914b0e210b3f2600b06baeddc3eeb18a217b01ffffffff0200c39dd0000000001976a914fd76b298e40d40a4e45a728c776641b2c71c194688ac002f6859000000001976a9141e4019c9b18f640c9fbb6fc621261eabd0d505df88ac00000000000000000000000000000000000000000000000000000000000000000000000000ffffffff")
    merkle_tx, cursor = serializer.deserialize(merkle_tx_data, 0)
    print merkle_tx
    merkle_tx_data_out = serializer.serialize(merkle_tx)
    print hexstr(merkle_tx_data_out)
