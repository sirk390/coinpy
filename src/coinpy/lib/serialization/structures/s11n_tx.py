# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder
from coinpy.lib.serialization.structures.s11n_tx_out import tx_out_encoder
from coinpy.lib.serialization.structures.s11n_tx_in import tx_in_encoder
from coinpy.model.protocol.structures.tx import tx

class tx_encoder(Encoder):
    TX = Structure([Field("<I", "version"),              
                    varsizelist_encoder(varint_encoder("txin_count"), tx_in_encoder()),
                    varsizelist_encoder(varint_encoder("txout_count"), tx_out_encoder()),
                    Field("<I", "lock_time")], "tx")

    def get_size(self, outpoint):
        return (self.TX.get_size(tx.version, tx.in_list, tx.out_list, tx.locktime))

    def encode(self, tx):
        return (self.TX.encode(tx.version, tx.in_list, tx.out_list, tx.locktime))

    def decode(self, data, cursor=0):
        (version, in_list, out_list, locktime), cursor = self.TX.decode(data, cursor)
        return (tx(version, in_list, out_list, locktime), cursor)

