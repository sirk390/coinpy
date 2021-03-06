from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.model.protocol.messages.getblocks import GetblocksMessage
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.structures.s11n_blocklocator import BlockLocatorSerializer

class GetblocksMessageSerializer(Serializer):
    GETBLOCKS = Structure([BlockLocatorSerializer(),
                           Uint256Serializer("stop")], "getblocks")
    
    def serialize(self, getblocks_msg):
        return (self.GETBLOCKS.serialize([getblocks_msg.block_locator,
                                          getblocks_msg.hash_stop]))

    def deserialize(self, data, cursor=0):
        (block_locator, hash_stop), cursor = self.GETBLOCKS.deserialize(data, cursor)
        return (GetblocksMessage(block_locator, hash_stop), cursor)


    
