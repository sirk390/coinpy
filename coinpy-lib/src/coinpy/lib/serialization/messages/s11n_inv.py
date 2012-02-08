# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.structures.s11n_invitem import InvitemSerializer
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.model.protocol.messages.inv import msg_inv

class InvMessageSerializer(Serializer):
    INV_ENCODER = VarsizelistSerializer(VarintSerializer(), 
                                        InvitemSerializer())
    
    def serialize(self, inv_msg):
        return (self.INV_ENCODER.serialize(inv_msg.items))
    
    def deserialize(self, data, cursor):
        invitems, cursor = self.INV_ENCODER.deserialize(data, cursor)
        return (msg_inv(invitems), cursor)