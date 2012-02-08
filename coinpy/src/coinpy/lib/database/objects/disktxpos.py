# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""

NULL_DISKTXPOS=4294967295

class DiskTxPos():
    def __init__(self, file=NULL_DISKTXPOS, blockpos=0, txpos=0):
        self.file, self.blockpos, self.txpos = file, blockpos, txpos
        
    def isnull(self):
        #when spent, CDiskTxPos.File is set to -1, main.h:135 IsNull() 
        return (self.file == NULL_DISKTXPOS)
    
    def setnull(self):
        self.file = NULL_DISKTXPOS
        
    def __str__(self):
        return ("DiskTxPos(file:%d,blockpos:%d,txpos:%d)" % (self.file, self.blockpos, self.txpos))
