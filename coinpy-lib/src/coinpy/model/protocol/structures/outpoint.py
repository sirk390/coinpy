# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from coinpy.model.protocol.structures.uint256 import Uint256

NULL_OUTPOINT_INDEX = 4294967295

class Outpoint():
    def __init__(self, hash, index):
        self.hash = hash  
        self.index = index          
    def is_null(self):
        return (self.hash == Uint256.zero() and self.index == NULL_OUTPOINT_INDEX)
    def __eq__(self, other):
        return (self.hash == other.hash and self.index == other.index)
    
    def __hash__(self):
        return (hash(self.hash) + hash(self.index))
    
    def __str__(self):
        return ("outpoint: hash:%s index:%d" % (self.hash, self.index))
