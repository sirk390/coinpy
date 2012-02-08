# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.getaddr import msg_getaddr
from coinpy.lib.serialization.common.serializer import Serializer

class GetAddrMessageSerializer(Serializer):
    def serialize(self, getaddr):
        return ("")
    
    def deserialize(self, data, cursor):
        return (msg_getaddr(), cursor)


    
