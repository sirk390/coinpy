# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_TX
from coinpy.model.protocol.messages.message import Message

class TxMessage(Message):
    def __init__(self, tx):
        super(TxMessage, self).__init__(MSG_TX)
        self.tx = tx
        
    def __str__(self):
        return ("msg_tx(%s)" % (str(self.tx)))

