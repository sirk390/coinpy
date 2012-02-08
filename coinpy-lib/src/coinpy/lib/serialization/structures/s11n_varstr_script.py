# -*- coding:utf-8 -*-
"""
Created on 3 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_varstr import VarstrSerializer
from coinpy.lib.serialization.scripts.serialize import ScriptSerializer
from coinpy.lib.serialization.common.serializer import Serializer

class VarstrScriptSerializer(Serializer):
    def __init__(self):
        self.serializer = ScriptSerializer()
        self.strencoder = VarstrSerializer()

    def encode(self, script):
        scriptstr = self.serializer.serialize(script)
        return (self.strencoder.encode(scriptstr))

    def get_size(self, script):
        #todo: fix algorithm
        return len(self.encode(script))

    def decode(self, data, cursor):
        scriptstr, newcursor = self.strencoder.decode(data, cursor)
        return (self.serializer.deserialize(scriptstr), newcursor)

