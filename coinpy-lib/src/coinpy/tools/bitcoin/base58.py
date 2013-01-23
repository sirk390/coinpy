#!/usr/bin/env python
from coinpy.tools.functools import count_leading_chars

b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
b58chars_values = dict((c, val) for val, c in enumerate(b58chars))

def base58encode(value, leading_zeros=None):
    result = ""
    while value != 0:
        div, mod = divmod(value, 58)
        result = b58chars[mod] + result
        value = div
    if leading_zeros:
        return b58chars[0] * leading_zeros + result
    return result

def base58decode(b58str):
    value = 0
    for c in b58str:
        value = value * 58 + b58chars_values[c]
    return (value)

def count_leading_base58_zeros(b58str):
    return count_leading_chars(b58str, b58chars[0])

if __name__ == '__main__':
    print base58encode(726378263726783267836783)
    print base58decode("9eDfMUZG7gNxGN")
    
    