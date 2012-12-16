from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.exceptions import MissingDataException

class VarstrSerializer(Serializer):
    def __init__(self, desc=""):
        self.lenfield = VarintSerializer()

    def serialize(self, str):
        return (self.lenfield.serialize(len(str)) + str)
    
    def get_size_for_len(self, i):
        return self.lenfield.get_size(i) + i
    
    def deserialize(self, data, cursor=0):
        length, newpos = self.lenfield.deserialize(data, cursor)
        #data = data[newpos:]
        if (length > len(data) - newpos):
            raise MissingDataException("Decoding error: not enough data for varstring (expected:%d, got:%d)" % (length, len(data) - newpos))
        return (data[newpos:newpos+length], newpos+length)
