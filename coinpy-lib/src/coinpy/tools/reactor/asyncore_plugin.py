# -*- coding:utf-8 -*-
"""
Created on 23 Apr 2012

@author: kris
"""
import asyncore

class AsyncorePlugin(object):
    def __init__(self):
        self.donework = False
    
    def install(self, reactor):
        # monkey patching asyncore
        save_send = asyncore.dispatcher.send
        save_recv = asyncore.dispatcher.recv
        def patched_send(self, data):
            self.donework = True
            return save_send(self, data)
        def patched_recv(self, buffer_size):
            self.donework = True
            return save_recv(self, buffer_size)
        asyncore.dispatcher.send = patched_send
        asyncore.dispatcher.recv = patched_recv
        
    def run(self):
        self.donework = False
        asyncore.loop(timeout=0, count=1)
        return self.donework

