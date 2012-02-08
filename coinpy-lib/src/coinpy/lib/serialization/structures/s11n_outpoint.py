# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.model.protocol.structures.outpoint import outpoint
from coinpy.lib.serialization.common.serializer import Serializer

class OutpointSerializer(Serializer):
    OUTPOINT = Structure([Uint256Serializer("hash"),
                          Field("<I","index")], "outpoint")

    def get_size(self, outpoint):
        return (self.OUTPOINT.get_size(outpoint.hash, outpoint.index))
    
    def serialize(self, outpoint):
        return (self.OUTPOINT.serialize(outpoint.hash, outpoint.index))

    def deserialize(self, data, cursor):
        (hash, index), cursor = self.OUTPOINT.deserialize(data, cursor)
        return (outpoint(hash, index), cursor)
