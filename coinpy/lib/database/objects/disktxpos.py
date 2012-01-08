# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""

class DiskTxPos():
    def __init__(self, file, blockpos, txpos):
        self.file, self.blockpos, self.txpos = file, blockpos, txpos
    def __str__(self):
        return ("DiskTxPos(file:%d,blockpos:%d,txpos:%d)" % (self.file, self.blockpos, self.txpos))
