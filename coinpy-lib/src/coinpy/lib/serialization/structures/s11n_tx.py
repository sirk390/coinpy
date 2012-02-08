# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.lib.serialization.structures.s11n_tx_out import TxoutSerializer
from coinpy.lib.serialization.structures.s11n_tx_in import TxinSerializer
from coinpy.model.protocol.structures.tx import tx

class TxSerializer(Serializer):
    TX = Structure([Field("<I", "version"),              
                    VarsizelistSerializer(VarintSerializer("txin_count"), TxinSerializer()),
                    VarsizelistSerializer(VarintSerializer("txout_count"), TxoutSerializer()),
                    Field("<I", "lock_time")], "tx")

    def get_size(self, tx):
        return (self.TX.get_size(tx.version, tx.in_list, tx.out_list, tx.locktime))

    def encode(self, tx):
        return (self.TX.encode(tx.version, tx.in_list, tx.out_list, tx.locktime))

    def decode(self, data, cursor=0):
        (version, in_list, out_list, locktime), cursor = self.TX.decode(data, cursor)
        return (tx(version, in_list, out_list, locktime), cursor)

