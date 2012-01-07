# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
import struct
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.exceptions import MissingDataException

class varint_encoder(Encoder):
    def __init__(self, desc=""):
        self.desc = desc
    
    def encode(self, value):
        if (value < 0xfd):
            return (struct.pack("<B", value))
        if (value <= 0xffff):
            return ("\xfd" + struct.pack("<H", value))
        if (value <= 0xffffffff):
            return ("\xfe" + struct.pack("<I", value))
        return ("\xff" + struct.pack("<Q", value))
    
    def decode(self, data, cursor):
        if (len(data) - cursor < 1):
            raise MissingDataException("Decoding error: not enough data for varint")
        prefix = struct.unpack_from("<B", data, cursor)[0]
        cursor += 1
        if (prefix < 0xFD):
            return (prefix, cursor)
        if (len(data) - cursor < {0xFD: 2, 0xFD: 4, 0xFD: 8}[prefix]):
            raise MissingDataException("Decoding error: not enough data for varint of type : %d" % (prefix))
        if (prefix == 0xFD):
            return (struct.unpack_from("<H", data, cursor)[0], cursor + 2)
        if (prefix == 0xFE):
            return (struct.unpack_from("<I", data, cursor)[0], cursor + 4)
        return (struct.unpack_from("<Q", data, cursor)[0], cursor + 8)
        
        