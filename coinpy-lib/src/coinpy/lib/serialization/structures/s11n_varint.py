# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
import struct
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.exceptions import MissingDataException

class VarintSerializer(Serializer):
    def __init__(self, desc=""):
        self.desc = desc
    
    def serialize(self, value):
        if (value < 0xfd):
            return (struct.pack("<B", value))
        if (value <= 0xffff):
            return ("\xfd" + struct.pack("<H", value))
        if (value <= 0xffffffff):
            return ("\xfe" + struct.pack("<I", value))
        return ("\xff" + struct.pack("<Q", value))
    
    def get_size(self, value):
        if (value < 0xfd):
            return (1)
        if (value <= 0xffff):
            return (3)
        if (value <= 0xffffffff):
            return (5)
        return (9)

    def deserialize(self, data, cursor):
        if (len(data) - cursor < 1):
            raise MissingDataException("Decoding error: not enough data for varint")
        prefix = struct.unpack_from("<B", data, cursor)[0]
        cursor += 1
        if (prefix < 0xFD):
            return (prefix, cursor)
        if (len(data) - cursor < {0xFD: 2, 0xFE: 4, 0xFF: 8}[prefix]):
            raise MissingDataException("Decoding error: not enough data for varint of type : %d" % (prefix))
        if (prefix == 0xFD):
            return (struct.unpack_from("<H", data, cursor)[0], cursor + 2)
        if (prefix == 0xFE):
            return (struct.unpack_from("<I", data, cursor)[0], cursor + 4)
        return (struct.unpack_from("<Q", data, cursor)[0], cursor + 8)
        
        