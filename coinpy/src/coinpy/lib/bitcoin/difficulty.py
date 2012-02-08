# -*- coding:utf-8 -*-
"""
Created on 7 Jan 2012

@author: kris
"""
from coinpy.model.constants.bitcoin import TARGET_INTERVAL
from coinpy.model.protocol.structures.uint256 import uint256

def uint256_difficulty(bits):
    exp, value = bits >> 24, bits & 0xFFFFFF
    return (uint256(value * 2 ** (8 * (exp - 3))))

def compact_difficulty(uin256num):
    shr = 0
    while ((uin256num.value >> (shr * 8)) > 0x7fffff):
        shr += 1
    exp, value = shr + 3, (uin256num.value >> (shr * 8) )
    return (exp << (3*8)| value)

