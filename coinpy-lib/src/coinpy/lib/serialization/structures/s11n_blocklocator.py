from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.model.protocol.structures.blocklocator import BlockLocator
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure

class BlockLocatorSerializer(Serializer):
    def __init__(self, flags=0):
        self.BLOCKLOCATOR = Structure([Field("<I", "version"),  
                                      VarsizelistSerializer(VarintSerializer("count"), Uint256Serializer("locator"))])

    def get_size(self, blocklocator):
        return (self.BLOCKLOCATOR.get_size([blocklocator.version, blocklocator.blockhashlist]))

    def serialize(self, blocklocator):
        return (self.BLOCKLOCATOR.serialize([blocklocator.version, blocklocator.blockhashlist]))

    def deserialize(self, data, cursor=0):
        (version, blockhashlist), cursor = self.BLOCKLOCATOR.deserialize(data, cursor)
        return (BlockLocator(version, blockhashlist), cursor)

        