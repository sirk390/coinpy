from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.model.protocol.messages.block import BlockMessage
from coinpy.lib.serialization.structures.s11n_block import BlockSerializer

class BlockMessageSerializer(Serializer):
    block_serializer = BlockSerializer()
    
    def __init__(self):    
        pass     
                                                      
    def serialize(self, block_msg):
        return (self.block_serializer.serialize(block_msg.block))
        
    def deserialize(self, data, cursor):
        block, cursor = self.block_serializer.deserialize(data, cursor)
        return (BlockMessage(block), cursor)

