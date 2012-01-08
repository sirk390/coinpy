# -*- coding:utf-8 -*-
"""
Created on 17 Nov 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_BLOCK, MSG_TX
from coinpy.lib.hash.hash_tx import hash_tx
from coinpy.tools.observer import Observable

class GetdataRequest(Observable):
    EVT_RECEIVED_HASH = Observable.createevent()
    EVT_COMPLETED = Observable.createevent()
    
    def __init__(self, peer, hashes):
        self.peer = peer
        self.hashes = hashes
        
    def start(self, node):    
        self.callbackid = node.add_callback((MSG_TX, self.peer), self.on_tx)        
         
    def on_tx(self, event):   
        hash = hash_tx(event.message.tx)
        if (hash in self.hashes):
            self.fire(self.EVT_RECEIVED_HASH, hash=hash)
            return (True)
        return (False)
    
    def stop(self):   
        self.node.del_callback(self.callbackid)      


