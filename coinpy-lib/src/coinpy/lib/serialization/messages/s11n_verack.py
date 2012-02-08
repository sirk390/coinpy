# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.verack import msg_verack
from coinpy.lib.serialization.common.serializer import Serializer

class VerackMessageSerializer(Serializer):
    def serialize(self, verack):
        return ("")
    
    def deserialize(self, data, cursor):
        return (msg_verack(), cursor)


    
