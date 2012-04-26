# -*- coding:utf-8 -*-
"""
Created on 25 Apr 2012

@author: kris
"""
from coinpy.tools.crypto.random.system_seeds import get_system_seeds
from coinpy.tools.crypto.ssl.ssl import ssl_RAND_add, ssl_RAND_bytes

class Random():
    def __init__(self):
        self.add_system_seeds()
        
    def add_system_seeds(self):
        for data, entropy in get_system_seeds():
            ssl_RAND_add(data, entropy)
    
    def get_random_bytes(self, length):
        return ssl_RAND_bytes(length)

if __name__ == '__main__':
    from coinpy.tools.hex import hexstr
    
    r = Random()
    print hexstr(r.get_random_bytes(100))
