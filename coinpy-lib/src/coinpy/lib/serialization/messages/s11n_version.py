# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.structures.s11n_netaddrfield import NetAddrSerializer
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.structures.s11n_varstr import VarstrSerializer
from coinpy.model.protocol.messages.version import msg_version
from coinpy.lib.serialization.common.serializer import Serializer

class VersionMessageSerializer(Serializer):
    VERSION_STRUCT = Structure([Field("<I", "version"),
                            Field("<Q", "services"),
                            Field("<Q","timestamp"),
                            NetAddrSerializer("addr_me"),
                            NetAddrSerializer("addr_you"), 
                            Field("<Q", "nonce"),
                            VarstrSerializer("sub_version_num"),
                            Field("<I", "start_height")], "version_message")
    
    def serialize(self, version_msg):
        return (self.VERSION_STRUCT.serialize(version_msg.version,
                                              version_msg.services,
                                              version_msg.timestamp,
                                              version_msg.addr_me,
                                              version_msg.addr_you,
                                              version_msg.nonce,
                                              version_msg.sub_version_num,
                                              version_msg.start_height))
    
    def deserialize(self, data, cursor):
        result, cursor = self.VERSION_STRUCT.deserialize(data, cursor)
        return (msg_version(*result), cursor)


    
