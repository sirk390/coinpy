# -*- coding:utf-8 -*-
"""
Created on 25 Jul 2011

@author: kris
"""

class TxInterface():
    def get_transaction(self):
        pass
    
    def get_block(self):
        pass

    def is_output_spent(self, output):
        pass
    
    def mark_spent(self, n):        
        pass
