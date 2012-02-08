# -*- coding:utf-8 -*-
"""
Created on 11 Sep 2011

@author: kris
"""

class VersionStatus():
    def __init__(self):
        self.version_sent = False
        self.version_received = False
        self.verack_received = False
        self.verack_sent = False
        self.version_message = None
        
    def versions_exchanged(self):
        return (self.version_sent and self.verack_received and self.version_received and self.verack_sent)
