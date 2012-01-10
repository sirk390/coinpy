# -*- coding:utf-8 -*-
"""
Created on 6 Jul 2011

@author: kris
"""
from coinpy.model.protocol.structures.uint256 import uint256

class BlockHeader():
    def __init__(self, version, hash_prev, hash_merkle, time, bits, nonce):
        self.version, self.hash_prev, self.hash_merkle, self.time, self.bits, self.nonce = version, hash_prev, hash_merkle, time, bits, nonce

    def target(self):
        exp, value = self.bits >> 24, self.bits & 0xFFFFFF
        return uint256(value * 2**(8*(exp - 3)))
                            
    def work(self):
        return ((1 << 256) / (self.target().value + 1))
        
    def __str__(self):
        return ("BlockHeader(version:%d,hash_next:%s,hash_merkle:%s,time:%d,bits:%d,nonce:%d)" % 
                    (self.version, 
                     self.hash_prev, 
                     self.hash_merkle, 
                     self.time,
                     self.bits,
                     self.nonce))
