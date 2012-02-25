# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_TX
from coinpy.model.protocol.messages.message import message

class msg_tx(message):
    def __init__(self, tx):
        message.__init__(self, MSG_TX)
        self.tx = tx
        
    def __str__(self):
        return ("msg_tx(%s)" % (str(self.tx)))

 