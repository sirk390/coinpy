# -*- coding:utf-8 -*-
"""
Created on 22 Apr 2012

@author: kris
"""
from coinpy.tools.reactor.reactor import reactor

class Future(object):
    def __init__(self):
        self.completed = False
        self.callback = None
        self.callback_args = ()
        self.success = None
        self.error = None
        self.result = None
        
    def set_error(self, exc):
        self.completed = True
        self.success = False
        self.error = exc
        if self.callback:
            reactor.call(self.callback, *self.callback_args, error=self.error, result=self.result)
        else:
            print self.error
            
    def set_result(self, result):
        self.completed = True
        self.success = True
        self.result = result
        if self.callback:
            reactor.call(self.callback, *self.callback_args, error=self.error, result=self.result)

    def set_callback(self, callback, callback_args=()):
        self.callback = callback
        self.callback_args = callback_args
