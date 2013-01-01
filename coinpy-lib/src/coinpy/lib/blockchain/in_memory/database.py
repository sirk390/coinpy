from coinpy.lib.transactions.hash_tx import hash_tx
from coinpy.lib.blocks.hash_block import hash_block
from coinpy.model.blockchain.blockchain_database import BlockChainDatabase,\
    TransactionNotFound, BlockNotFound
from coinpy.lib.blockchain.in_memory.transaction_handle import InMemoryTransactionHandle
from coinpy.lib.blockchain.in_memory.block_handle import InMemoryBlockHandle

class InMemoryBlockchainDatabase(BlockChainDatabase):
    def __init__(self, blocks):
        self.blocks = []
        self.indexed_blocks = {}
        self.block_heights = {}
        self.indexed_tx = {}
        self.next_main_chain = {}
        self.tx_blkhashes = {} # {tx_hash => blockhash}
        self.spend_outputs = {} # {tx_hash => [list of None/Uint256]}
        for block in blocks:
            self.append_block(block)

                    
    def contains_block(self, block_hash):
        return block_hash in self.indexed_blocks
    
    def contains_transaction(self, txhash):
        return txhash in self.indexed_tx

    def get_block_handle(self, block_hash):
        if not block_hash in self.indexed_blocks:
            raise BlockNotFound(str(block_hash))
        return InMemoryBlockHandle(self.indexed_blocks[block_hash], self.block_heights[block_hash])
    
    def get_transaction_handle(self, txhash):
        if txhash not in self.indexed_tx:
            raise TransactionNotFound(str(txhash))
        return InMemoryTransactionHandle(self.indexed_tx[txhash], 
                                         self.tx_blkhashes[txhash],
                                         self.spend_outputs[txhash])

    def get_next_in_mainchain(self, blockhash):
        if blockhash not in self.next_main_chain:
            raise BlockNotFound(str(blockhash))
        return self.next_main_chain[blockhash]

    def append_block(self, block):
        """
        """
        blkhash = hash_block(block)
        self.indexed_blocks[blkhash] = block
        self.block_heights[blkhash] = len(self.blocks)
        if self.blocks:
            self.next_main_chain[hash_block(self.blocks[-1])] = blkhash
        self.next_main_chain[hash_block(block)] = None
        self.blocks.append(block)
        for tx in block.transactions:
            txhash = hash_tx(tx)
            self.indexed_tx[txhash] = tx
            self.tx_blkhashes[txhash] = blkhash
            self.spend_outputs[txhash] = [None] * len(tx.out_list)
            if not tx.iscoinbase():
                for txin in tx.in_list:
                    self.spend_outputs[txin.previous_output.hash][txin.previous_output.index] = txhash
                    
    def pop_block(self):
        """
         raises
            RemovingGenesisException: if the blockchain only contains the genesis block.
        """
        block = self.blocks.pop()
        blkhash = hash_block(block)
        #remove indexes
        del self.next_main_chain[blkhash]
        self.next_main_chain[block.blockheader.hash_prev] = None
        del self.indexed_blocks[blkhash]
        del self.block_heights[blkhash]
        for tx in block.transactions:
            txhash = hash_tx(tx)
            if not tx.iscoinbase():
                for txin in tx.in_list:
                    self.spend_outputs[txin.previous_output.hash][txin.previous_output.index] = None
            del self.indexed_tx[txhash]
            del self.tx_blkhashes[txhash]
            del self.spend_outputs[txhash]
        return block

    def get_best_hash(self):
        return hash_block(self.blocks[-1])
    
    def get_genesis_hash(self):
        return hash_block(self.blocks[0])

