# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.lib.serialization.exceptions import MissingDataException

class varstr_encoder(Encoder):
    def __init__(self, desc=""):
        super(varstr_encoder, self).__init__(desc)
        self.lenfield = varint_encoder()

    def encode(self, str):
        result = self.lenfield.encode(len(str))
        result += str
        return (result)

    def decode(self, data, cursor):
        length, newpos = self.lenfield.decode(data, cursor)
         #data = data[newpos:]
        if (length > len(data) - newpos):
            raise MissingDataException("Decoding error: not enough data for varstring (expected:%d, got:%d)" % (length, len(data) - newpos))
        return (data[newpos:newpos+length], newpos+length)
