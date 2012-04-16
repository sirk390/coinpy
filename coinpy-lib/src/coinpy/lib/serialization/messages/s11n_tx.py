# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.model.protocol.messages.tx import TxMessage
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer

class TxMessageSerializer(Serializer):
    def __init__(self):    
        self.txencoder = TxSerializer()
     
    def serialize(self, txmsg):
        return (self.txencoder.serialize(txmsg.tx))

    def deserialize(self, data, cursor=0):
        tx, cursor = self.txencoder.deserialize(data, cursor)
        return (TxMessage(tx), cursor)

