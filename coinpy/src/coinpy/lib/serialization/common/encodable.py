# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""

class Encoder(object):
    def __init__(self, desc=""):
        self.desc = desc
    def encode(self, value):
        pass
    def decode(self, data, cursor):
        return ("", cursor)
        