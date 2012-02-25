# -*- coding:utf-8 -*-
"""
Created on 7 Feb 2012

@author: kris
"""
from coinpy.tools.bitcoin.base256 import base256decode, base256encode

MAX_NUM_SIZE = 4

def cast_to_bool(val):
    if len(val) == 0:
        return False
    if any(c != 0 for c in val[:-1]):
        return True
    #allow negative zero
    if val[:-1] == 0x80:
        return False
    return True

def cast_to_number(val):
    if (len(val) > MAX_NUM_SIZE):
        raise Exception("cast_to_number() : overflow")
    return (base256decode(val))


def valtype_from_number(val):
    return (base256encode(val))

def valtype_from_boolean(val):
    if val:
        return ("\x01")
    return ("\x00")

if __name__ == '__main__':
    print cast_to_number(valtype_from_boolean(True))
    
