from coinpy.model.protocol.structures.uint256 import Uint256
import struct
from coinpy.lib.serialization.exceptions import MissingDataException
from coinpy.lib.serialization.common.serializer import Serializer

class Uint256Serializer(Serializer):
    def __init__(self, desc=""):
        self.desc = desc

    def serialize(self, uint256val):
        return (struct.pack("32s", uint256val.get_bytestr()))
    
    def get_size(self, value):
        return (32)
    
    def deserialize(self, data, cursor=0):
        if (len(data) - cursor) < 32:
            raise MissingDataException("%s: Not enought data for uint256" % (self.desc))
        bytestr, = struct.unpack_from("32s", data, cursor)
        return (Uint256.from_bytestr(bytestr), cursor + 32)
