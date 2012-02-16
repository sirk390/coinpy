# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from collections import namedtuple

class SockAddr(namedtuple("SockAddr", "ip port")):
    def __str__(self):
        return ("%s:%d" % (self.ip, self.port))
    def __eq__(self, other):
        return (self.ip == other.ip and self.port == other.port)
    def __hash__(self):
        return hash(self.ip) + hash(self.port)
    