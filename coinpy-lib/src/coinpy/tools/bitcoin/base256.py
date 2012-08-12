# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""

# Make a big endian bytestring from an integer.
def base256encode(value, pad=None):
    result_bytes = []
    while value != 0:
        div, mod = divmod(value, 256)
        result_bytes.append(chr(mod))
        value = div
    return ("".join(result_bytes[::-1]).rjust(pad or 0, "\0"))

# Make an integer from a big endian bytestring.
def base256decode(bytestr):
    value = 0
    for b in bytestr:
        value = value * 256 + ord(b)
    return (value)

def base256decode_le_signed(bytestr):
    if len(bytestr) == 0:
        return 0
    b0 = ord(bytestr[-1])
    value = (b0 & 0b1111111)
    for b in bytestr[-2::-1]:
        value = value * 256 + ord(b)
    if (b0 & 0b10000000):
        value = -value
    return (value)

def base256encode_le_signed(value):
    absvalue = abs(value)
        
    result_bytes = []
    while absvalue != 0:
        div, mod = divmod(absvalue, 256)
        result_bytes.append(mod)
        absvalue = div
    if value < 0 and result_bytes[-1] & 0x80:
        result_bytes.append(0x80)
    elif value > 0 and result_bytes[-1] & 0x80:
        result_bytes.append(0x00)
    elif value < 0:
        result_bytes[-1] = result_bytes[-1] | 0x80
    return ("".join(chr(b) for b in result_bytes))

if __name__ == '__main__':
    #from coinpy.tools.hex import hexstr
    #print hexstr(base256encode(8728178917894516516))

    print base256decode("\x01\x00")
    
