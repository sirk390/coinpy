# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.structures.s11n_netaddrfield import NetAddrField
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.structures.s11n_varstr import varstr_encoder
from coinpy.model.protocol.messages.version import msg_version
from coinpy.lib.serialization.common.encodable import Encoder

class version_encoder(Encoder):
    VERSION_STRUCT = Structure([Field("<I", "version"),
                            Field("<Q", "services"),
                            Field("<Q","timestamp"),
                            NetAddrField("addr_me"),
                            NetAddrField("addr_you"), 
                            Field("<Q", "nonce"),
                            varstr_encoder("sub_version_num"),
                            Field("<I", "start_height")], "version_message")
    
    def encode(self, version_msg):
        return (self.VERSION_STRUCT.encode(version_msg.version,
                                      version_msg.services,
                                      version_msg.timestamp,
                                      version_msg.addr_me,
                                      version_msg.addr_you,
                                      version_msg.nonce,
                                      version_msg.sub_version_num,
                                      version_msg.start_height))
    
    def decode(self, data, cursor):
        result, cursor = self.VERSION_STRUCT.decode(data, cursor)
        return (msg_version(*result), cursor)


    
