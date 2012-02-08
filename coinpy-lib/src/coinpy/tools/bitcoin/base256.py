# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""

# Make a big endian bytestring from an integer.
def base256encode(value, pad=None):
    result = b""
    while value != 0:
        div, mod = divmod(value, 256)
        result = chr(mod) + result
        value = div
    return (result.rjust(pad or 0, "\0"))

# Make an integer from a big endian bytestring.
def base256decode(bytestr):
    value = 0
    for b in bytestr:
        value = value * 256 + ord(b)
    return (value)

if __name__ == '__main__':
    from coinpy.tools.hex import hexstr
    print hexstr(base256encode(8728178917894516516))

