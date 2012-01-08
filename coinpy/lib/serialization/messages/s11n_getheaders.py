# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.model.protocol.messages.getheaders import msg_getheaders

class getheaders_encoder(Encoder):
    GETHEADERS = Structure([varint_encoder(),
                           Field("32s", "hash_start"),
                           Field("32s","hash_stop")], "getheaders")

    def encode(self, getheaders_msg):
        return (self.GETHEADERS.encode(getheaders_msg.version,
                                       getheaders_msg.hash_start,
                                       getheaders_msg.hash_stop))

    def decode(self, data, cursor):
        version, hash_start, hash_stop = self.GETHEADERS.decode(data, cursor)
        return (msg_getheaders(version, hash_start, hash_stop), cursor)

