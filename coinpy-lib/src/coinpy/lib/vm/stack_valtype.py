# -*- coding:utf-8 -*-
"""
Created on 7 Feb 2012

@author: kris
"""
from coinpy.tools.bitcoin.base256 import base256decode, base256encode,\
    base256decode_le_signed, base256encode_le_signed
from coinpy.tools.hex import hexstr

MAX_NUM_SIZE = 4

def cast_to_bool(val):
    if len(val) == 0:
        return False
    if any(ord(c) != 0 for c in val[:-1]):
        return True
    #allow negative zero
    if ord(val[-1]) == 0x80 or ord(val[-1]) == 0:
        return False
    return True

def cast_to_number(val):
    if (len(val) > MAX_NUM_SIZE):
        raise Exception("cast_to_number() : overflow (size={size})".format(size=len(val)))
    return (base256decode_le_signed(val))


def valtype_from_number(val):
    return (base256encode_le_signed(val))

def valtype_from_boolean(val):
    if val:
        return ("\x01")
    return ("\x00")


if __name__ == '__main__':
    """print cast_to_number("\xff\xff\xff\xff")
    print 0xffffffff
    print cast_to_number("\xff\xff\xff\x7f")
    print cast_to_number("\x82")

    print "a" """
    #OP_PUSHDATA(4):ffffff7f,OP_NEGATE,OP_DUP,OP_ADD,OP_PUSHDATA(5):feffffff80,OP_EQUAL
    #OP_PUSHDATA(4):ffffff7f,OP_DUP,OP_ADD OP_PUSHDATA(5):feffffff00,OP_EQUAL
    valtype_from_number(0)
    print cast_to_number("\xff\xff\xff\x7f") * 2

    print cast_to_number("\x02")
    print cast_to_number("\x82")
    print "V", valtype_from_number(0), "V"
    print hexstr(valtype_from_number(4294967294))
    print hexstr(valtype_from_number(cast_to_number("\xff\xff\xff\xff")))
    print hexstr(valtype_from_number(cast_to_number("\xff\xff\xff\xff") + cast_to_number("\xff\xff\xff\xff")))
    print cast_to_number("\xff\xff\xff\x7f")
    
    
    a = -cast_to_number("\xff\xff\xff\x7f")
    print "-a:", hexstr(valtype_from_number(-cast_to_number("\xff\xff\xff\x7f")))
    print "2a:", a+a
    print "2a_hex:",hexstr(valtype_from_number(a+a))
    print cast_to_number("\xff\xff\xff\x7f")
    print hexstr(valtype_from_number(-cast_to_number("\xff\xff\xff\x7f")))
    #print cast_to_number("\xfe\xff\xff\xff\x80")

"""

OP_0,OP_PUSHDATA(4):ffffffff,OP_PUSHDATA(4):ffffff7f OP_WITHIN


[-2147483519, -4294967167L, 0


OP_PUSHDATA(4):ffffff7f,OP_NEGATE,OP_DUP,OP_ADD OP_PUSHDATA(5):feffffff80,OP_EQUAL



"""