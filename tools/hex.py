# -*- coding:utf-8 -*-
"""
Created on 13 Jun 2011

@author: kris
"""

def printablechar(c):
    return ((32 <= ord(c) <= 126) and c or ".")

def printablestr(chars):
    return ''.join(printablechar(c) for c in chars)

def hexstr(data, sep=""):
    return sep.join(["%02x" % ord(c) for c in data])

def decodehexstr(data, sep=""):
    bytelen = 2 + len(sep)
    size = len(data) / bytelen 
    return ("".join(chr(int(data[i*bytelen:(i+1)*bytelen], 16)) for i in range(size)))     

def hexdumpline(line, width=16, sep=" "):
    return (hexstr(line, sep) + (sep * (3 * (width - len(line))))) + sep + printablestr(line)

def hexdump(data, width=16, sep=" "):
    nlines, leftover = divmod(len(data), width)
    result = ""
    for pos in range(nlines):
        result += hexdumpline(data[pos*width:(pos+1)*width]) + "\n"
    if (leftover != 0):
        result += hexdumpline(data[nlines*width:])
    return result



if __name__ == '__main__':
    print hexdump("aaaaaaaaaazdaojazzzadaop")
    
    print hexstr("abcdef")
    print decodehexstr("616263646566")
    