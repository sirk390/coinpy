# -*- coding:utf-8 -*-
"""
Created on 26 Jul 2011

@author: kris
"""

class Block():
    def __init__(self,
                 blockheader,
                 transactions):
        self.blockheader = blockheader
        self.transactions = transactions
        self.rawdata = None
    
    def __str__(self):
        return ("Block(%s, transactions(%d)[%s...])" % 
                    (str(self.blockheader), 
                     len(self.transactions),
                     ",".join([str(t) for t in self.transactions[:5]])))
 

