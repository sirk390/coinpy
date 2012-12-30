from coinpy.lib.transactions.hash_tx import hash_tx
from coinpy.lib.blocks.hash_block import hash_block
from coinpy.model.blockchain.tx_handle import TxHandle
from coinpy.model.blockchain.blockchain_database import OutputNotSpend

class InMemoryTransactionHandle(TxHandle):
    def __init__(self, tx, blk_hash, spend_outputs):
        """
        spend_outputs (list of None or Uint256 of length len(tx.out_list))
        """
        self.tx = tx
        self.blk_hash = blk_hash
        self.spend_outputs = spend_outputs
        
    def get_transaction(self):
        return self.tx

    def get_block_hash(self):
        return self.blk_hash
                
    def is_output_spent(self, n):
        return self.spend_outputs[n] is not None

    def get_spending_transaction_hash(self, n):
        spent = self.spend_outputs[n]
        if spent is None:
            raise OutputNotSpend(str(n))
        return spent
            
    def output_count(self):
        return (len(self.tx.out_list))
    
    def mark_spent(self, n, in_tx_hash):
        self.spend_outputs[n] = in_tx_hash
       
    def mark_unspent(self, n):
        self.spend_outputs[n] = None
    