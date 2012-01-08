# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_GETDATA
from coinpy.model.protocol.messages.message import message

class msg_getdata(message):
    def __init__(self, 
                 invitems):
        super(msg_getdata, self).__init__(MSG_GETDATA)       
        self.invitems = invitems
        
    def __str__(self):
        return ("getdata invitems:%s" % (str(self.invitems)))
