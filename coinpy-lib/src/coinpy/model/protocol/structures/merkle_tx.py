# -*- coding:utf-8 -*-
"""
Created on 15 Feb 2012

@author: kris
"""

""" A transaction with a merkle branch linking it to the blockchain

    tx: transaction
    nindex: int 
"""
class MerkleTx():
    def __init__(self, tx, blockhash, merkle_branch, nindex):
        self.tx = tx
        self.blockhash = blockhash
        self.merkle_branch = merkle_branch
        self.nindex = nindex
        
    def __str__(self):
        return ("MerkleTx(tx:%s, block:%s, merkle_branch(%d):%s..., nindex:%d)" % (str(self.tx), str(self.blockhash), len(self.merkle_branch), ",".join(str(h) for h in self.merkle_branch[:5]), self.nindex))