# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.model.protocol.messages.getdata import msg_getdata
from coinpy.lib.serialization.structures.s11n_invitem import InvitemSerializer
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer

class GetdataMessageSerializer(Serializer):
    GETDATA_ENC = VarsizelistSerializer(VarintSerializer(), 
                                        InvitemSerializer())
    
    def encode(self, getdata_msg):
        return (self.GETDATA_ENC.encode(getdata_msg.invitems))

    def decode(self, data, cursor):
        invitems, cursor = self.GETDATA_ENC.decode(data, cursor)
        return (msg_getdata(invitems))

    
