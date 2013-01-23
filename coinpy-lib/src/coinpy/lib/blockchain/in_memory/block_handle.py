from coinpy.lib.transactions.hash_tx import hash_tx
from coinpy.lib.blocks.hash_block import hash_block
from coinpy.model.blockchain.block_handle import BlockHandle

class InMemoryBlockHandle(BlockHandle):
    def __init__(self, hash, block, height):
        self.hash = hash
        self.block = block
        self.height = height
        
    def get_block(self):
        return self.block
    
    def get_height(self):
        return self.height

    def get_blockheader(self):
        return self.block.blockheader
    
    def get_hash(self):
        return self.hash