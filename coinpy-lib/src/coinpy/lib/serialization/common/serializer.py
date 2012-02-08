# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""

class Serializer(object):
    def __init__(self, desc=""):
        self.desc = desc
    def serialize(self, value):
        pass
    def deserialize(self, data, cursor):
        return ("", cursor)
    def get_size(self):
        pass 