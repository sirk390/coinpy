# -*- coding:utf-8 -*-
"""
Created on 13 Jan 2012

@author: kris
"""
from coinpy.model.blockchain.txinterface import TxInterface

class SimulatedTx(TxInterface):
    def __init__(self, tx, block, outputs_spent=[]):
        self.tx = tx
        self.block = block
        self.outputs_spent = set(outputs_spent)
        
    def get_transaction(self):
        return self.tx
    
    def get_block(self):
        return self.block

    def is_spent(self, n):
        return (n in self.outputs_spent)
    
    def mark_spent(self, n):
        self.outputs_spent.add(n)
        
    