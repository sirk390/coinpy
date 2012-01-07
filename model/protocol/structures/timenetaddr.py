# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""

"""
    timestamped netaddr
"""
class timenetaddr():
    def __init__(self, timestamp, netaddr):
        self.timestamp = timestamp  
        self.netaddr = netaddr
        
    def __str__(self):
        return ("%d:%s" % (self.timestamp, str(self.netaddr)))
