# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.scripts.serialize import ScriptSerializer

class tx_in():
    NSEQUENCE_FINAL = 4294967295 #2**32-1
    
    def __init__(self, previous_output, script, sequence):
        self.previous_output = previous_output  
        self.script = script          
        self.sequence = sequence
                
    def isfinal(self):
        return (self.sequence == self.NSEQUENCE_FINAL)
    
    def __str__(self):
        return ("tx_in: %s %s sequence:%d" % (self.previous_output, str(self.script), self.sequence))
