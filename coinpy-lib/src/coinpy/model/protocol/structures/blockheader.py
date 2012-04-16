# -*- coding:utf-8 -*-
"""
Created on 6 Jul 2011

@author: kris
"""
from coinpy.model.protocol.structures.uint256 import Uint256

class BlockHeader():
    def __init__(self, version, hash_prev, hash_merkle, time, bits, nonce):
        self.version, self.hash_prev, self.hash_merkle, self.time, self.bits, self.nonce = version, hash_prev, hash_merkle, time, bits, nonce
        # optional extra fields used to cache the hash value once computed
        self.hash = None
        self.rawdata = None

    def target(self):
        exp, value = self.bits >> 24, self.bits & 0xFFFFFF
        return Uint256.from_bignum(value * 2**(8*(exp - 3)))
                            
    def work(self):
        return ((1 << 256) / (self.target().get_bignum() + 1))
        
    def __str__(self):
        return ("BlockHeader(version:%d,hash_prev:%s,hash_merkle:%s,time:%d,bits:%d,nonce:%d)" % 
                    (self.version, 
                     self.hash_prev, 
                     self.hash_merkle, 
                     self.time,
                     self.bits,
                     self.nonce))
