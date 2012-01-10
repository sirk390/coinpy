# -*- coding:utf-8 -*-
"""
Created on 2 Jul 2011

@author: kris
"""

#uint256.to_bytestr
def base256encode(value, pad=None):
    result = b""
    while value != 0:
        div, mod = divmod(value, 256)
        result = chr(mod) + result
        value = div
    return (result.rjust(pad or 0, "\0"))

#uint256.from_bytestr
def base256decode(bytestr):
    value = 0
    for b in bytestr:
        value = value * 256 + ord(b)
    return (value)

if __name__ == '__main__':
    from coinpy.tools.hex import hexstr
    print hexstr(base256encode(8728178917894516516))

