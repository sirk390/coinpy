# -*- coding:utf-8 -*-
"""
Created on 6 Mar 2012

@author: kris
"""

''' 
    Output for which we have a keypair
'''
class ControlledOutput():
    def __init__(self, txhash, index, txout, keypair):
        self.txhash = txhash
        self.index = index
        self.txout = txout
        self.keypair = keypair
