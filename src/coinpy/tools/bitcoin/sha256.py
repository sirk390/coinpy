# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
import hashlib
    
def doublesha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def double_sha256_2_input(data1, data2):
    h = hashlib.sha256()
    h.update(data1)
    h.update(data2)
    return hashlib.sha256(h.digest()).digest()

def sha256checksum(data):
    return (doublesha256(data)[0:4])

if __name__ == '__main__':
    from coinpy.tools.hex import hexstr
    print hexstr(sha256checksum(""))
