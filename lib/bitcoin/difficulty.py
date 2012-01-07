# -*- coding:utf-8 -*-
"""
Created on 7 Jan 2012

@author: kris
"""
from coinpy.model.constants.bitcoin import TARGET_INTERVAL

def uint256_difficulty(bits):
    exp, value = bits >> 24, bits & 0xFFFFFF
    return (value * 2 ** (8 * (exp - 3)))

def compact_difficulty(bignum):
    shr = 0
    while ((bignum >> (shr * 8)) > 0x7fffff):
        shr += 1
    exp, value = shr + 3, (bignum >> (shr * 8) )
    return (exp << (3*8)| value)


if __name__ == '__main__':
    print "exp:", 0x1b0404cb >> 24
    print ("%064x" % uint256_difficulty(0x1b0404cb))
    print ("%08x" % compact_difficulty(0x00000000000404cb000000000000000000000000000000000000000000000000))
    
    print ("%064x" % uint256_difficulty(0x1d00ffff))
    print ("%08x" % compact_difficulty(0x00000000FFFF0000000000000000000000000000000000000000000000000000))
    #1cffff00
