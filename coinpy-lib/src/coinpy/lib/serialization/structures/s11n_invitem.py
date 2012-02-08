# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from coinpy.model.protocol.structures.invitem import INV_ITEMS, invitem
from coinpy.lib.serialization.exceptions import FormatErrorException
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.structures.s11n_uint256 import uint256_encoder

class invitem_encoder():
    INVITEM_ENC = Structure([Field("<I", "type"),
                             uint256_encoder("hash")], "getblocks")

    def get_size(self, invitem):
        return (self.INVITEM_ENC.get_size(invitem.type,
                                          invitem.hash))
    def encode(self, invitem):
        return (self.INVITEM_ENC.encode(invitem.type, invitem.hash))

    def decode(self, data, cursor):
        (type, hash), cursor = self.INVITEM_ENC.decode(data, cursor)
        if (type not in INV_ITEMS):
            raise FormatErrorException("Unknown inventory item")
        return (invitem(type, hash), cursor)

