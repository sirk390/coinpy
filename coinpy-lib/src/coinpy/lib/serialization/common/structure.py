import struct
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer

class Structure(Serializer):
    def __init__(self, fields, desc="", flags=0):
        super(Structure, self).__init__(desc)
        self.fields = fields
        self.flags = flags

    def serialize(self, args):
        return ("".join(field.serialize(value) for value, field in zip(args, self.fields)))

    def get_size(self, args):
        return sum(field.get_size(value) for value, field in zip(args, self.fields))
    
    def deserialize(self, data, cursor):
        results = []
        for field in self.fields:
            value, cursor = field.deserialize(data, cursor)
            results.append(value)
        return (results, cursor)

