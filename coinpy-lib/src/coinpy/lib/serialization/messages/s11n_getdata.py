# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.model.protocol.messages.getdata import msg_getdata
from coinpy.lib.serialization.structures.s11n_invitem import invitem_encoder
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder

class getdata_encoder(Encoder):
    GETDATA_ENC = varsizelist_encoder( varint_encoder(), 
                                       invitem_encoder())
    
    def encode(self, getdata_msg):
        return (self.GETDATA_ENC.encode(getdata_msg.invitems))

    def decode(self, data, cursor):
        invitems, cursor = self.GETDATA_ENC.decode(data, cursor)
        return (msg_getdata(invitems))

    
