class TransactionNotFound(Exception):
    pass
class BlockNotFound(Exception):
    pass
class OutputNotSpend(Exception):
    pass
#ValueError ? e.g. ValueError: empty range for randrange() (1,1, 0)

class BlockChainDatabase():
    def contains_block(self, block_hash):
        """Return (bool) if the blockchain contains a given block hash"""
        
    def contains_transaction(self, transaction_hash):
        """Return (bool) if the blockchain contains a given transaction hash"""
    
    def get_block_handle(self, block_hash):
        """Return (BlockHandle) the handle for `block_hash`
        
           raises BlockNotFound
        """
        pass
        
    def get_transaction_handle(self, transaction_hash):
        """Return (TxHandle) the handle for a transaction hash.
        
           raises TransactionNotFound
        """
        pass
    
    def get_next_in_mainchain(self, blockhash):
        """Return (Uint256) the hash of the next `blockhash` in the chain.
           Return None if blockhash == best_hash

        raises
            BlockNotFound if the hash doesn't exist
        """
        pass
    
    def append_block(self, blockhash, block):
        pass

    def pop_block(self):
        """IndexError if empty"""
        pass
    
    def get_best_hash(self):
        pass
    
    def get_genesis_hash(self):
        pass

