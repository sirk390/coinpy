# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.tx_in import TxIn
from coinpy.lib.serialization.structures.s11n_outpoint import OutpointSerializer
from coinpy.lib.serialization.structures.s11n_varstr_script import VarstrScriptSerializer
from coinpy.lib.serialization.common.serializer import Serializer


class TxinSerializer(Serializer):
    TXIN = Structure([OutpointSerializer(),
                      VarstrScriptSerializer(),
                      Field("<I","sequence")], "outpoint")
    
    def get_size(self, txin):
        return (self.TXIN.get_size([txin.previous_output, txin.script, txin.sequence]))

    def serialize(self, txin):
        return (self.TXIN.serialize([txin.previous_output, txin.script, txin.sequence]))

    def deserialize(self, data, cursor):
        (previous_output, script, sequence), cursor = self.TXIN.deserialize(data, cursor)
        return (TxIn(previous_output, script, sequence), cursor)


