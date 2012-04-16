# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from coinpy.model.protocol.structures.invitem import INV_ITEMS, Invitem
from coinpy.lib.serialization.exceptions import FormatErrorException
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.common.serializer import Serializer

class InvitemSerializer(Serializer):
    INVITEM_ENC = Structure([Field("<I", "type"),
                             Uint256Serializer("hash")], "getblocks")

    def get_size(self, invitem):
        return (self.INVITEM_ENC.get_size(invitem.type,
                                          invitem.hash))
    def serialize(self, invitem):
        return (self.INVITEM_ENC.serialize([invitem.type, invitem.hash]))

    def deserialize(self, data, cursor):
        (type, hash), cursor = self.INVITEM_ENC.deserialize(data, cursor)
        if (type not in INV_ITEMS):
            raise FormatErrorException("Unknown inventory item")
        return (Invitem(type, hash), cursor)

