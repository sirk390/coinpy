# -*- coding:utf-8 -*-
"""
Created on 3 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_varstr import varstr_encoder
from coinpy.lib.serialization.scripts.serialize import ScriptSerializer

class varstr_script_encoder():
    def __init__(self):
        self.serializer = ScriptSerializer()
        self.strencoder = varstr_encoder()

    def encode(self, script):
        scriptstr = self.serializer.serialize(script)
        return (self.strencoder.encode(scriptstr))

    def decode(self, data, cursor):
        scriptstr, newcursor = self.strencoder.decode(data, cursor)
        return (self.serializer.deserialize(scriptstr), newcursor)

