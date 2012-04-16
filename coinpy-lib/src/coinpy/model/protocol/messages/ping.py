# -*- coding:utf-8 -*-
"""
Created on 21 Feb 2012

@author: kris
"""
from coinpy.model.protocol.messages.message import Message
from coinpy.model.protocol.messages.types import MSG_PING

class PingMessage(Message):
    def __init__(self):
        super(PingMessage, self).__init__(MSG_PING)       
            
    def __str__(self):
        return ("PingMessage()")
