# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_GETHEADERS
from coinpy.model.protocol.messages.message import Message

class GetheadersMessage(Message):
    def __init__(self, 
                 start_count,
                 hash_start,
                 hash_stop):
        super(message, self).__init__(MSG_GETHEADERS)       
        self.start_count = start_count
        self.hash_start = hash_start
        self.hash_stop = hash_stop    
            
    def __str__(self):
        return ("getheaders count:%d, start:%s, stop:%s" % (self.start_count, self.hash_start, self.hash_stop))
