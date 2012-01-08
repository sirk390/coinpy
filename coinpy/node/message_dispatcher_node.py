# -*- coding:utf-8 -*-
"""
Created on 7 Dec 2011

@author: kris
"""
from coinpy.node.node import Node
from coinpy.model.protocol.messages.types import MESSAGE_TYPES, MSG_INV
from coinpy.node.versionned_node import VersionnedNode
from coinpy.node.defines import MessageProcessed
import heapq
from coinpy.model.protocol.structures.invitem import INV_BLOCK, INV_TX
from coinpy.node.dispatch_status import DispatchStatus
import collections

class MessageDispatcherNode(VersionnedNode):
    def __init__(self, reactor, get_blockchain_height, params, log):
        super(MessageDispatcherNode, self).__init__(reactor, lambda : 0, params, log)
        self.log = log
        self.handlers = {}
        self.subscribe(Node.EVT_MESSAGE, self.__on_message)
        self.in_progress = []
    ''' 
        selector:      
                        MESSAGE_TYPES:   message_type
                  or    tuple:          (MSG_INV, INV_TX/INV_BLOCK)
    '''
    def add_handler(self, message_type, method):
        self.handlers[message_type] = method
        #self.handlers[message_type].append(method)
        #heapq.heappush(self.handlers[selector], (priority, method)) 
       
    def remove_handler(self, method):
        pass
    
    def __on_message(self, event):
        #handle messages 
        messages = {event.message.type : event.message } #{selector =>  [message ...], ... }
        if (event.message.type in self.handlers):
            self.handlers[event.message.type](event.handler, event.message)
        #also handle exploded invs
        if (event.message.type == MSG_INV):
            for item in event.message.items:
                if ((MSG_INV, item.type) in self.handlers):
                    self.handlers[(MSG_INV, item.type)](event.handler, item)
