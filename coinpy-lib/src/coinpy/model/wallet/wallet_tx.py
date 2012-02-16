# -*- coding:utf-8 -*-
"""
Created on 11 Feb 2012

@author: kris
"""
from coinpy.tools.hex import hexstr

class WalletTx(object):
    def __init__(self, hash, tx):
        self.hash, self.tx = hash, tx
    
    def __str__(self):
        return "hash:%s tx:%s" % (str(self.hash), str(self.tx))
