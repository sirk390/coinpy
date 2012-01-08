# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.model.protocol.structures.uint256 import uint256
import struct
from coinpy.lib.serialization.exceptions import MissingDataException

class uint256_encoder():
    def __init__(self, desc):
        self.desc = desc

    def encode(self, uint256val):
        return (struct.pack("32s", uint256val.to_bytestr()))
    
    def decode(self, data, cursor):
        if (len(data) - cursor) < 32:
            raise MissingDataException("%s: Not enought data for uint256" % (self.desc))
        bytestr, = struct.unpack_from("32s", data, cursor)
        return (uint256.from_bytestr(bytestr), cursor + 32)
