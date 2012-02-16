# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""

class BlockLocator():
    def __init__(self, version, blockhashlist):
        self.version = version
        self.blockhashlist = blockhashlist
    def __str__(self):
        return "BlockLocator(len=%d hashes=%s..., version=%d)" % (len(self.blockhashlist), ",".join(str(h) for h in self.blockhashlist[:5]), self.version)
