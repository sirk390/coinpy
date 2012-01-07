# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_GETADDR
from coinpy.model.protocol.messages.message import message

class msg_getaddr(message):
    def __init__(self):
        super(msg_getaddr, self).__init__(MSG_GETADDR)       
        
    def __str__(self):
        return ("getaddr")

