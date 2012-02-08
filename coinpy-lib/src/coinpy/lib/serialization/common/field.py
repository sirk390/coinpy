import struct
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.exceptions import MissingDataException

class Field(Serializer):
    def __init__(self, format, desc, options=0):
        super(Field, self).__init__(desc)
        self.format = format
        self.size = struct.calcsize(format)
 
    def get_size(self, value):
        return self.size
    
    def encode(self, value):
        return (struct.pack(self.format, value))

    def decode(self, data, cursor):
        if (len(data) - cursor) < self.size:
            raise MissingDataException("Decoding error: not enough data for field %s (type: %s)" % (self.desc, self.format))
        return (struct.unpack_from(self.format, data, cursor)[0], cursor + self.size)

