# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer

class VarsizelistSerializer(Serializer):
    def __init__(self, count_serializer, element_serializer):
        self.count_serializer = count_serializer
        self.element_serializer = element_serializer

    def serialize(self, lst):
        result = self.count_serializer.serialize(len(lst))
        for elm in lst:
            result += self.element_serializer.serialize(elm)
        return (result)

    def get_size(self, lst):
        return self.count_serializer.get_size(len(lst)) + sum(self.element_serializer.get_size(value) for value in lst)

    def deserialize(self, data, cursor):
        length, cursor = self.count_serializer.deserialize(data, cursor)
        elms = []
        for _ in range(length):
            value, cursor = self.element_serializer.deserialize(data, cursor)
            elms.append(value)
        return (elms, cursor)
