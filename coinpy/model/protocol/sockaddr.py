# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from collections import namedtuple

class SockAddr(namedtuple("SockAddr", "ip port")):
    def __str__(self):
        return ("%s:%d" % (self.ip, self.port))
