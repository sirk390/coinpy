# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_INV
from coinpy.model.protocol.messages.message import message 

class msg_inv(message):
    def __init__(self, items):
        super(msg_inv, self).__init__(MSG_INV)
        self.items = items
        
    def __str__(self):
        return ("inv(%d): %s..." % (len(self.items), " ".join([str(i) for i in self.items[0:10]]))) 
