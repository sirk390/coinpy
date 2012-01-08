# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from coinpy.model.constants.bitcoin import COIN

class tx_out():
    def __init__(self, value, script):
        self.value = value  
        self.script = script          
       
    def __str__(self):
        return ("tx_out: value:%s %s" % (self.value * 1.0 / COIN, str(self.script)))
