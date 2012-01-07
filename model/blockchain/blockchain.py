# -*- coding:utf-8 -*-
"""
Created on 25 Jul 2011

@author: kris
"""
class BlockChain():
    def contains_block(self, block_hash):
        pass
    
    def contains_transaction(self, transaction_hash):
        pass
    
    def get_block_iterator(self, block_hash):
        pass
    
    def get_transaction_iterator(self, transaction_hash):
        pass
    

    def addblock(self, block):
        pass
        
    def is_orphan_transaction(self, transaction):
        for txin in transaction.in_list:
            out = txin.previous_output
            if (not self.blockchain.contains_transaction(out.hash)):
                return (True)
        return (False)
    
    def is_orphan_block(self, block):
        if (not self.blockchain.contains_block(block.prev_block)):
            return (True)
        return (False)
    
    def verifyblock(self, block):
        return (False)

    def getheight(self):
        return (0)