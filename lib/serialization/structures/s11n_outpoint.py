# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.structures.s11n_uint256 import uint256_encoder
from coinpy.model.protocol.structures.outpoint import outpoint

class outpoint_encoder():
    OUTPOINT = Structure([uint256_encoder("hash"),
                          Field("<I","index")], "outpoint")

    def encode(self, outpoint):
        return (self.OUTPOINT.encode(outpoint.hash, outpoint.index))

    def decode(self, data, cursor):
        (hash, index), cursor = self.OUTPOINT.decode(data, cursor)
        return (outpoint(hash, index), cursor)
