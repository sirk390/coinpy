# -*- coding:utf-8 -*-
"""
Created on 27 Jan 2012

@author: kris
"""

class MemBlockHandle():
    def __init__(self, block, height):
        self.block = block
        self.height = height
            
    def get_block(self):
        return self.block

    def get_blockheader(self):
        return self.block.blockheader

    def get_height(self):
        return self.height
  
    