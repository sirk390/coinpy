# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer

class VarsizelistSerializer(Serializer):
    def __init__(self, count_encoder, element_encoder):
        self.count_encoder = count_encoder
        self.element_encoder = element_encoder

    def encode(self, lst):
        result = self.count_encoder.encode(len(lst))
        for elm in lst:
            result += self.element_encoder.encode(elm)
        return (result)

    def get_size(self, lst):
        return self.count_encoder.get_size(len(lst)) + sum(self.element_encoder.get_size(value) for value in lst)

    def decode(self, data, cursor):
        length, cursor = self.count_encoder.decode(data, cursor)
        elms = []
        for _ in range(length):
            value, cursor = self.element_encoder.decode(data, cursor)
            elms.append(value)
        return (elms, cursor)
