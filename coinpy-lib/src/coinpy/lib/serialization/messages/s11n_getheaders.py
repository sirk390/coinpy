# -*- coding:utf-8 -*-
"""
Created on 23 Jun 2011

@author: kris
"""

from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.model.protocol.messages.getheaders import GetheadersMessage

class GetheadersMessageSerializer(Serializer):
    GETHEADERS = Structure([VarintSerializer(),
                           Field("32s", "hash_start"),
                           Field("32s","hash_stop")], "getheaders")

    def serialize(self, getheaders_msg):
        return (self.GETHEADERS.serialize([getheaders_msg.version,
                                           getheaders_msg.hash_start,
                                           getheaders_msg.hash_stop]))

    def deserialize(self, data, cursor):
        version, hash_start, hash_stop = self.GETHEADERS.deserialize(data, cursor)
        return (GetheadersMessage(version, hash_start, hash_stop), cursor)

