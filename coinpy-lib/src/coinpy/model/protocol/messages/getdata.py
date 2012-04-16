# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_GETDATA
from coinpy.model.protocol.messages.message import Message

class GetdataMessage(Message):
    def __init__(self, 
                 invitems):
        super(GetdataMessage, self).__init__(MSG_GETDATA)       
        self.invitems = invitems
        
    def __str__(self):
        return ("getdata invitems(%d)[%s...]" % (len(self.invitems), ",".join(str(i) for i in self.invitems[:5])))
