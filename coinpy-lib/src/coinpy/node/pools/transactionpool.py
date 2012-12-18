from coinpy.tools.observer import Observable
from coinpy.lib.transactions.hash_tx import hash_tx

class TransactionPool(Observable):
    EVT_ADDED_TX = Observable.createevent()
    EVT_REMOVED_TX = Observable.createevent()

    def __init__(self):
        Observable.__init__(self)
        self.txs = {}
        self.spent_outpoints = {} # outpoint => (txhash, in_index)
        
    def add_tx(self, txhash, tx):
        self.txs[txhash] = tx
        # todo: 1/ check for conflicts / replace transactions
        # 2/ check for non-standard pay-to-script-hash in inputs
        # 3/ check minimum fees
        self.fire(self.EVT_ADDED_TX, hash=txhash)
    
    def remove_tx(self, txhash):
        del self.txs[txhash]
        self.fire(self.EVT_REMOVED_TX, hash=txhash)

    def has_conflicts(self, tx):
        for txout in tx.out_list:
            if txout.previous_output in self.spent_outpoints:
                return
        
    def contains_transaction(self, txhash):
        return (txhash in self.txs)
    
    def get_transaction(self, txhash):
        return self.txs[txhash]
