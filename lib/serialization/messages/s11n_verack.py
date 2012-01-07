# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.verack import msg_verack
from coinpy.lib.serialization.common.encodable import Encoder

class verack_encoder(Encoder):
    def encode(self, verack):
        return ("")
    
    def decode(self, data, cursor):
        return (msg_verack(), cursor)


    
