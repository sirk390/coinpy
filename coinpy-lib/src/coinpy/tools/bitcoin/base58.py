#!/usr/bin/env python

b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
b58chars_values = dict((c, val) for val, c in enumerate(b58chars))

def base58encode(value):
    result = ""
    while value != 0:
        div, mod = divmod(value, 58)
        result = b58chars[mod] + result
        value = div
    return result

def base58decode(b58str):
    value = 0
    for c in b58str:
        value = value * 58 + b58chars_values[c]
    return (value)

if __name__ == '__main__':
    print base58encode(726378263726783267836783)
    print base58decode("9eDfMUZG7gNxGN")
    
    