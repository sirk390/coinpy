class TxHandle():
    def get_transaction(self):
        pass
    
    def get_block(self):
        pass

    def is_output_spent(self, output):
        pass
    
    def mark_spent(self, n, is_spent, in_tx_hash=None):
        pass
