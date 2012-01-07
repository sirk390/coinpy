# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""

class outpoint():
    def __init__(self, hash, index):
        self.hash = hash  
        self.index = index          
       
    def __str__(self):
        return ("outpoint: hash:%s index:%d" % (self.hash, self.index))
