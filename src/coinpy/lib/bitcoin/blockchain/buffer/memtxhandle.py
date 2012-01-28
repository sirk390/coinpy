# -*- coding:utf-8 -*-
"""
Created on 19 Jan 2012

@author: kris
"""
from coinpy.model.blockchain.txinterface import TxInterface

class MemTxHandle(TxInterface):
    def __init__(self, hash, tx, block, outputs_spent):
        self.hash = hash
        self.tx = tx
        self.block = block
        self.outputs_spent = outputs_spent
        self.modified = False
        
    def get_transaction(self):
        return self.tx
    
    def get_block(self):
        return self.block

    def is_output_spent(self, n):
        is_spent, _ = self.outputs_spent[n]
        return is_spent
    
    def mark_spent(self, n, is_spent, in_tx_hash=None):
        self.outputs_spent[n] = (is_spent, in_tx_hash)
        self.modified = True

