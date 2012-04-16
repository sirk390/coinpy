# -*- coding:utf-8 -*-
"""
Created on 21 Feb 2012

@author: kris
"""


from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.model.protocol.messages.ping import PingMessage

class PingMessageSerializer(Serializer):
    def serialize(self, ping_message):
        return ("")
    
    def deserialize(self, data, cursor):
        return (PingMessage(), cursor)


    
