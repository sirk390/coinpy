# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.structures.s11n_ipaddrfield import IPAddrField
from coinpy.model.protocol.structures.netaddr import netaddr


class NetAddrField(Structure):
    def __init__(self, desc):
        fields = [Field("<Q", "services"),
                  IPAddrField("ip"),
                  Field(">H", "port")]
        super(NetAddrField, self).__init__(fields, desc)

    def encode(self, a_netaddr):
        data = super(NetAddrField, self).encode(a_netaddr.services, a_netaddr.ip, a_netaddr.port)
        return (data)

    def decode(self, data, cursor):
        (services, ip, port), cursor = super(NetAddrField, self).decode(data, cursor)
        return (netaddr(services, ip, port), cursor)

