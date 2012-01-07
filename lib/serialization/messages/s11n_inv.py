# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.lib.serialization.structures.s11n_invitem import invitem_encoder
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder
from coinpy.model.protocol.messages.inv import msg_inv

class inv_encoder(Encoder):
    INV_ENCODER = varsizelist_encoder( varint_encoder(), 
                                       invitem_encoder())
    
    def encode(self, inv_msg):
        return (self.INV_ENCODER.encode(inv_msg.items))
    
    def decode(self, data, cursor):
        invitems, cursor = self.INV_ENCODER.decode(data, cursor)
        return (msg_inv(invitems), cursor)
