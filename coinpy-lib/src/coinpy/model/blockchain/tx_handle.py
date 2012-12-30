class TxHandle():
    """ TxHandle interface """
    def get_transaction(self):
        """ Return (Tx) the transaction """
        pass

    def get_block_hash(self):
        """ Return (Uint256) the hash of the block containing the transaction"""
        pass
                
    def is_output_spent(self, n):
        """ Return (bool) if output `n`(int) is spent"""
        pass

    def get_spending_transactionu_hash(self, n):
        """ Return (Uint256) if output `n` is spent """
        pass
            
    def output_count(self):
        """ Return (int) the number of outputs """
        pass
    
    def mark_spent(self, n, is_spent, in_tx_hash=None):
        """ Mark outputs `n` (int) as spent """
        pass