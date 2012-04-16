# -*- coding:utf-8 -*-
"""
Created on 26 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varstr import VarstrSerializer
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.messages.alert import AlertMessage

class AlertMessageSerializer(Serializer):
    ALERT = Structure([VarstrSerializer("payload"),
                       VarstrSerializer("signature")])
    
    def serialize(self, alert_msg):
        return (self.ALERT.serialize([alert_msg.payload, alert_msg.signature]))

    def deserialize(self, data, cursor):
        (payload, signature), cursor = self.ALERT.deserialize(data, cursor)
        return (AlertMessage(payload, signature), cursor)


    
