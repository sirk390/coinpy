# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.tx_out import TxOut
from coinpy.lib.serialization.structures.s11n_varstr_script import VarstrScriptSerializer
from coinpy.lib.serialization.common.serializer import Serializer

class TxoutSerializer(Serializer):
    TXOUT = Structure([Field("<q","value"),
                       VarstrScriptSerializer()], "outpoint")

    def get_size(self, txout):
        return (self.TXOUT.get_size([txout.value, txout.script]))

    def serialize(self, outpoint):
        return (self.TXOUT.serialize([outpoint.value, outpoint.script]))

    def deserialize(self, data, cursor):
        (value, script), cursor = self.TXOUT.deserialize(data, cursor)
        return (TxOut(value, script), cursor)


