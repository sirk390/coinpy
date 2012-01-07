import struct
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.exceptions import MissingDataException

class Field(Encoder):
    def __init__(self, format, desc, options=0):
        super(Field, self).__init__(desc)
        self.format = format
        self.size = struct.calcsize(format)
        self.setoptions(options)

    def setoptions(self, options):
        pass
 
    def encode(self, value):
        return (struct.pack(self.format, value))

    def decode(self, data, cursor):
        if (len(data) - cursor) < self.size:
            raise MissingDataException("Decoding error: not enough data for field %s (type: %s)" % (self.desc, self.format))
        return (struct.unpack_from(self.format, data, cursor)[0], cursor + self.size)

