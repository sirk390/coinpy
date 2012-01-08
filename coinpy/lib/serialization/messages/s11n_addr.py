# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder
from coinpy.lib.serialization.structures.s11n_timenetaddr import timenetaddr_encoder
from coinpy.model.protocol.messages.addr import addr_msg

class addr_encoder(Encoder):
    ADDR = varsizelist_encoder(varint_encoder("count"),
                               timenetaddr_encoder())
    
    def encode(self, addr_msg):
        return (self.ADDR.encode(addr_msg.addr_list))

    def decode(self, data, cursor):
        addr_list, cursor = self.ADDR.decode(data, cursor)
        return (addr_msg(addr_list), cursor)


    
