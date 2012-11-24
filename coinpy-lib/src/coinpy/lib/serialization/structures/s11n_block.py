from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.model.protocol.structures.block import Block
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer

class BlockSerializer(Serializer):
    def __init__(self, flags=0):
        self.BLOCK = Structure([BlockheaderSerializer(flags), 
                                VarsizelistSerializer(VarintSerializer("txn_count"), TxSerializer())], "block")

    def get_size(self, block):
        return (self.BLOCK.get_size([block.blockheader,
                                     block.transactions]))

    def serialize(self, block):
        return (self.BLOCK.serialize([block.blockheader,
                                      block.transactions]))
        
    def deserialize(self, data, cursor):
        (blockheader, transactions), new_cursor = self.BLOCK.deserialize(data, cursor)
        block = Block(blockheader, transactions)
        block.rawdata = data[cursor:new_cursor]
        return (block, new_cursor)

