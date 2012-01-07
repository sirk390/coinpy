# -*- coding:utf-8 -*-
"""
Created on 26 Jul 2011

@author: kris
"""

class DbTxIndex():
    def __init__(self, version, pos, spent):
        self.version, self.pos, self.spent  = version, pos, spent
     
    def is_output_spent(self, output):
        #when spent, CDiskTxPos.File is set to -1, main.h:135 IsNull() 
        return (self.txindex.spent[output].file == -1)
    
    def __str__(self):
        return ("DbTxIndex(ver:%d,pos:%s,spent(%d):[%s...])" % 
                    (self.version, 
                     str(self.pos), 
                     len(self.spent), 
                     ",".join([str(i) for i in self.spent[0:5]])))
