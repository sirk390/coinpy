import struct
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.encodable import Encoder

class Structure(Encoder):
    def __init__(self, fields, desc, flags=0):
        super(Structure, self).__init__(desc)
        self.fields = fields
        self.flags = flags

    def encode(self, *args):
        result = ""
        for value, field in zip(args, self.fields):
            enc = field.encode(value)
            result += enc
        return (result)

    def get_size(self, *args):
        return sum(field.get_size(value) for value, field in zip(args, self.fields))
    
    def decode(self, data, cursor):
        results = []
        for field in self.fields:
            value, cursor = field.decode(data, cursor)
            results.append(value)
        return (results, cursor)

