# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.encodable import Encoder
from coinpy.lib.serialization.exceptions import MissingDataException, FormatErrorException
import struct

class IPAddrField(Encoder):
    IP6HEADER = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF"
    def __init__(self, desc):
        super(IPAddrField, self).__init__(desc)
        
    def encode(self, ip):
        return (self.IP6HEADER + struct.pack(">4B", *[int(b) for b in ip.split(".")]))
    
    def decode(self, data, cursor):
        if (len(data) - cursor < 16):
            raise MissingDataException("Decoding error: not enough data for ip address")
        if (data[cursor:cursor+12] != IPAddrField.IP6HEADER):
            raise FormatErrorException("Decoding error: ip header doesn't match : ipv6 not supported")
        return (".".join(str(b) for b in struct.unpack(">4B", data[cursor+12:cursor+16])), cursor+16)
