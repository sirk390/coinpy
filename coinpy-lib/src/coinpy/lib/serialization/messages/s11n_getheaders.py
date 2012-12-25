from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.model.protocol.messages.getheaders import GetheadersMessage
from coinpy.lib.serialization.structures.s11n_blocklocator import BlockLocatorSerializer
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer

class GetheadersMessageSerializer(Serializer):
    GETHEADERS = Structure([BlockLocatorSerializer(),
                            Uint256Serializer()])

    def serialize(self, getheaders_msg):
        return (self.GETHEADERS.serialize([getheaders_msg.blocklocator,
                                           getheaders_msg.hash_stop]))

    def deserialize(self, data, cursor=0):
        (blocklocator, hash_stop), cursor = self.GETHEADERS.deserialize(data, cursor)
        return (GetheadersMessage(blocklocator, hash_stop), cursor)

