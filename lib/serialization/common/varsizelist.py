# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
class varsizelist_encoder():
    def __init__(self, count_encoder, element_encoder):
        self.count_encoder = count_encoder
        self.element_encoder = element_encoder

    def encode(self, lst):
        result = self.count_encoder.encode(len(lst))
        for elm in lst:
            result += self.element_encoder.encode(elm)
        return (result)

    def decode(self, data, cursor):
        length, cursor = self.count_encoder.decode(data, cursor)
        elms = []
        for _ in range(length):
            value, cursor = self.element_encoder.decode(data, cursor)
            elms.append(value)
        return (elms, cursor)
