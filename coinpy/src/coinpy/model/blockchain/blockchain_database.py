# -*- coding:utf-8 -*-
"""
Created on 25 Jul 2011

@author: kris
"""

class BlockChainDatabase():
    def contains_block(self, block_hash):
        pass
        
    def contains_transaction(self, transaction_hash):
        pass
    
    def get_block_handle(self, block_hash):
        pass
        
    def get_transaction_handle(self, transaction_hash):
        pass
    
    def saveblock(self, blockhash, block):
        pass

    def set_mainchain(self, mainchainhash):
        pass

    def get_mainchain(self):
        pass

