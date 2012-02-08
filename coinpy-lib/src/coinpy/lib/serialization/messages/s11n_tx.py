# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.model.protocol.messages.tx import msg_tx
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer

class TxMessageSerializer(Serializer):
    def __init__(self):    
        self.txencoder = TxSerializer()
     
    def encode(self, txmsg):
        return (self.txencoder.encode(txmsg.tx))

    def decode(self, data, cursor=0):
        tx, cursor = self.txencoder.decode(data, cursor)
        return (msg_tx(tx), cursor)

