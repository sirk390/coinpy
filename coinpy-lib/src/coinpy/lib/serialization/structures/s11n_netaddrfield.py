# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.structures.s11n_ipaddrfield import IPAddrSerializer
from coinpy.model.protocol.structures.netaddr import netaddr
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.common.structure import Structure


class NetAddrSerializer(Serializer):
    def __init__(self, desc):
        self.NETADDR = Structure([Field("<Q", "services"),
                                  IPAddrSerializer("ip"),
                                  Field(">H", "port")], "netaddr")
        pass

    def encode(self, a_netaddr):
        data = self.NETADDR.encode(a_netaddr.services, a_netaddr.ip, a_netaddr.port)
        return (data)

    def decode(self, data, cursor):
        (services, ip, port), cursor = self.NETADDR.decode(data, cursor)
        return (netaddr(services, ip, port), cursor)

