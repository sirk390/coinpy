# -*- coding:utf-8 -*-
"""
Created on 17 Nov 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_INV, MSG_BLOCK
from coinpy.model.protocol.structures.invitem import INV_BLOCK

class GetBlocksRequest():
    EVT_RECEIVED_INV = Observable.createevent()
     
    def __init__(self, downloader, peer, peer_height, blocklocator_hashes, on_receive_hash):
        self.client_height = peer_height
        self.blocklocator_hashes = blocklocator_hashes
        self.received_hashes = []
        
        downloader.push_handler(MSG_INV, self.on_inv)
      
    def start(self, node):    
        self.callbackid = node.add_callback((MSG_INV, self.peer), self.on_inv)        
          
    def on_inv(self, event):   
        self.received_hashes.append(event.item.hash)
        self.fire(self.EVT_RECEIVED_INV, hash=event.item.hash)
        downloader.request.append( GetdataBlockRequest() )

   
    def stop(self):   
        self.node.del_callback(self.callbackid)
