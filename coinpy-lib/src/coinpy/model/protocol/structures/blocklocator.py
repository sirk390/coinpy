# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""

"""
    starts with the highest block, ends with the genesis block 
    (dense and the beginning but then sparse)
"""
class BlockLocator():
    def __init__(self, version, blockhashlist):
        self.version = version
        self.blockhashlist = blockhashlist
    
    def highest(self):
        return self.blockhashlist[0]
    
    def lowest(self):
        return self.blockhashlist[-1]
    
    def __str__(self):
        return "BlockLocator(len=%d hashes=%s..., version=%d)" % (len(self.blockhashlist), ",".join(str(h) for h in self.blockhashlist[:5]), self.version)
