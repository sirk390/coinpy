# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from coinpy.model.protocol.structures.uint256 import uint256

NULL_OUTPOINT_INDEX = 4294967295

class outpoint():
    def __init__(self, hash, index):
        self.hash = hash  
        self.index = index          
    def is_null(self):
        return (self.hash == uint256(0) and self.index == NULL_OUTPOINT_INDEX)
    def __str__(self):
        return ("outpoint: hash:%s index:%d" % (self.hash, self.index))
