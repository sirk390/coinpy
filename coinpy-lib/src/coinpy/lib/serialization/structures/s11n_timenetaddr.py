# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.timenetaddr import Timenetaddr
from coinpy.lib.serialization.structures.s11n_netaddrfield import NetAddrSerializer
from coinpy.lib.serialization.common.serializer import Serializer

class TimenetaddrSerializer(Serializer):
    TIME_NETADDR = Structure([Field("<I", "timestamp"),
                              NetAddrSerializer("addr")], "timestamped_netaddr")

    def serialize(self, timenetaddr):
        return (self.TIME_NETADDR.serialize([timenetaddr.timestamp, timenetaddr.netaddr]))

    def deserialize(self, data, cursor):
        (timestamp, netaddr), cursor = self.TIME_NETADDR.deserialize(data, cursor)
        return (Timenetaddr(timestamp, netaddr), cursor)
