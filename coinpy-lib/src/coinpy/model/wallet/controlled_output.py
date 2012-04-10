# -*- coding:utf-8 -*-
"""
Created on 6 Mar 2012

@author: kris
"""

''' 
    Output for which we have a keypair
'''
class ControlledOutput():
    def __init__(self, txhash, tx, index, txout, keypair):
        self.txhash = txhash
        self.tx = tx
        self.index = index
        self.txout = txout
        self.keypair = keypair
        
    def __str__(self):
        return ("%s:%d (key:%s)" % (self.txhash, self.index, str(self.keypair)))
    