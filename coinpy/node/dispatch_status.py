# -*- coding:utf-8 -*-
"""
Created on 12 Dec 2011

@author: kris
"""

class DispatchStatus():
    Unhandled, Processing, Processed = range(3)
    def __init__(self, peer, message, handlers):
        self.peer = peer
        self.message = message
        self.handlers = handlers
        self.status = self.Unhandled
        
    def set_status(self, status):
        self.status = status
        
    def processed(self):
        self.status = self.Processed
        
    def inprogress(self):
        self.status = self.Processing
