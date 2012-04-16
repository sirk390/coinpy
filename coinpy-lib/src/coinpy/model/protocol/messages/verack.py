# -*- coding:utf-8 -*-
"""
Created on 18 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_VERACK
from coinpy.model.protocol.messages.message import Message 

class VerackMessage(Message):
    def __init__(self):
        super(VerackMessage, self).__init__(MSG_VERACK)
        
    def __str__(self):
        return ("verack.") 
