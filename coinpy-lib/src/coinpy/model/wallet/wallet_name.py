# -*- coding:utf-8 -*-
"""
Created on 11 Feb 2012

@author: kris
"""

class WalletName(object):
    def __init__(self, name, address):
        self.name, self.address = name, address
        
    def __str__(self):
        return "WalletName(%s:%s)" % (self.name, str(self.address))
