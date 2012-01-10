# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
class uint256():
    def __init__(self, value):
        self.value = value
        
    @staticmethod
    def from_bytestr(bytstr):
        value = 0
        for b in bytstr[::-1]:
            value = value * 256 + ord(b)
        return (uint256(value))

    @staticmethod
    def from_hexstr(hexstr):
        return (uint256(int(hexstr, 16)))

    def to_hexstr(self):
        return ("%064x" % (self.value))
    
    def to_bytestr(self):
        value, result = self.value, ""
        while value != 0:
            div, mod = divmod(value, 256)
            result = chr(mod) + result
            value = div
        return (result.rjust(32, "\0")[::-1])

    def __str__(self):
        return (self.to_hexstr())
    def __eq__(self, other):
        return self.value == other.value
    def __cmp__(self, other):
        return (cmp(self.value, other.value))
    def __ne__(self, other):
        return self.value != other.value
    def __hash__(self):
        return hash(self.value)
        
if __name__ == '__main__':
    a = uint256.from_hexstr("2d216583913526ace30f51687f3fb0b1d416faef805c8d7bcb6b1b8331f34af8")
    b = uint256.from_hexstr("00000000098bce17bb6a38cf3c35edccf57e692d0a93d7e6a650eeaf28c79")
    print a.value
    print a
    print uint256(a.value)
    print uint256.from_bytstr(a.to_bytestr())
    print "".join(["%02x" % ord(c) for c in a.to_bytestr()[::-1]])
    print uint256.from_hexstr("98bce17bb6a38cf3c35edccf57e692d0a93d7e6a650eeaf28c79030000000000")
    print (b)
    print uint256.from_bytstr(b.to_bytestr())
    