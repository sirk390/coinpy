# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.tx_in import tx_in
from coinpy.lib.serialization.structures.s11n_outpoint import outpoint_encoder
from coinpy.lib.serialization.structures.s11n_varstr_script import varstr_script_encoder


class tx_in_encoder():
    TXIN = Structure([outpoint_encoder(),
                      varstr_script_encoder(),
                      Field("<I","sequence")], "outpoint")
    TXIN2 = Structure([outpoint_encoder(),
                      varstr_script_encoder()], "outpoint")
    
    def get_size(self, txin):
        return (self.TXIN.get_size(txin.previous_output, txin.script, txin.sequence))

    def encode(self, txin):
        #Tmp FIXME
        return (self.TXIN.encode(txin.previous_output, txin.script, txin.sequence))
        #return (self.TXIN2.encode(txin.previous_output, txin.script))

    def decode(self, data, cursor):
        (previous_output, script, sequence), cursor = self.TXIN.decode(data, cursor)
        return (tx_in(previous_output, script, sequence), cursor)


