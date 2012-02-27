# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.tools.hex import decodehexstr
from coinpy.tools.bitcoin.base256 import base256encode

class uint256():
    def __init__(self, bytestr=None):
        #internal representation: little endian 32 byte string
        self.bytestr = bytestr
    
    @staticmethod
    def zero():
        return uint256("\0" * 32)
    
    @staticmethod
    def from_bytestr(bytestr):
        return uint256(bytestr=bytestr)
    
    #input big endian hexstr
    @staticmethod
    def from_hexstr(hexstr):
        return (uint256(decodehexstr(hexstr)[::-1]))

    @staticmethod
    def from_bignum(value):
        return (uint256(base256encode(value, 32)[::-1]))

    def get_hexstr(self):
        return "".join(("%02x" % ord(c)) for c in self.bytestr[::-1])
        #return ("%064x" % (self.value))

    def get_bignum(self):
        value = 0
        for b in self.bytestr[::-1]:
            value = value * 256 + ord(b)
        return (value)
    
    def get_bytestr(self):
        return self.bytestr
        '''value, result = self.value, ""
        while value != 0:
            div, mod = divmod(value, 256)
            result = chr(mod) + result
            value = div
        return (result.rjust(32, "\0")[::-1])'''

    def __str__(self):
        return (self.get_hexstr())
    def __eq__(self, other):
        return self.bytestr == other.bytestr
    def __cmp__(self, other):
        return (cmp(self.get_bignum(), other.get_bignum()))
    def __ne__(self, other):
        return self.bytestr != other.bytestr
    def __hash__(self):
        return hash(self.bytestr)
        
if __name__ == '__main__':
    a = uint256.from_hexstr("2d216583913526ace30f51687f3fb0b1d416faef805c8d7bcb6b1b8331f34af8")
    b = uint256.from_hexstr("00000000098bce17bb6a38cf3c35edccf57e692d0a93d7e6a650eeaf28c79")

    print a.get_bignum()
    print uint256.from_bytestr(a.get_bytestr())
    print "".join(["%02x" % ord(c) for c in a.get_bytestr()[::-1]])
    print uint256.from_hexstr("98bce17bb6a38cf3c35edccf57e692d0a93d7e6a650eeaf28c79030000000000")
    print (b)
    print uint256.from_bytestr(b.get_bytestr())
    