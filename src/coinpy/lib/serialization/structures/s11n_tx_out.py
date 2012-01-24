# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.tx_out import tx_out
from coinpy.lib.serialization.structures.s11n_varstr_script import varstr_script_encoder

class tx_out_encoder():
    TXOUT = Structure([Field("<Q","value"),
                       varstr_script_encoder()], "outpoint")

    def get_size(self, txout):
        return (self.TXOUT.get_size(txout.value, txout.script))

    def encode(self, outpoint):
        return (self.TXOUT.encode(outpoint.value, outpoint.script))

    def decode(self, data, cursor):
        (value, script), cursor = self.TXOUT.decode(data, cursor)
        return (tx_out(value, script), cursor)


