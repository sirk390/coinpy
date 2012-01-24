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
    
    def get_block(self, block_hash):
        pass
    
    def get_branch(self, lasthash, firsthash=None):
        pass
    
    def get_transaction(self, transaction_hash):
        pass
    
    def saveblock(self, blockhash, block):
        pass

    def getheight(self):
        return (0)

