# -*- coding:utf-8 -*-
"""
Created on 14 Dec 2011

@author: kris
"""

'''
    list of linked blocks used in BlockPool

'''
class LinkedBlockList():
    def __init__(self, sender, hash, block):
        self.prevhash = block.blockheader.hash_prev
        self.endhash = hash
        self.blocks = [(sender, block)]
    
    def append_block(self, sender, hash, block):
        self.endhash = hash
        self.blocks.append( (sender, block) )
    
    def append_list(self, blocklist):
        self.endhash = blocklist.endhash
        self.blocks += blocklist.blocks
    
    def __len__(self):
        return len(self.blocks)

