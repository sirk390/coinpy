# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.getaddr import msg_getaddr
from coinpy.lib.serialization.common.encodable import Encoder

class getaddr_encoder(Encoder):
    def encode(self, getaddr):
        return ("")
    
    def decode(self, data, cursor):
        return (msg_getaddr(), cursor)


    
