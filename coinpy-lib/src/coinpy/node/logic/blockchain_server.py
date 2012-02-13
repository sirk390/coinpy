# -*- coding:utf-8 -*-
"""
Created on 13 Sep 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_GETDATA, MSG_GETBLOCKS,\
    MSG_GETHEADERS, MSG_INV, MSG_TX, MSG_BLOCK, MSG_HEADERS
from coinpy.node.node import Node
from coinpy.tools.observer import Observable
from coinpy.node.version_exchange_node import VersionExchangeNode


class BlockchainServer(Observable):
    def __init__(self, node, blockchain, log):
        super(BlockchainServer, self).__init__()
        
        node.subscribe(VersionExchangeNode.EVT_VERSION_EXCHANGED, self.on_version_exchanged)      
        node.subscribe((Node.EVT_MESSAGE, MSG_GETDATA), self.on_getdata)
        node.subscribe((Node.EVT_MESSAGE, MSG_GETBLOCKS), self.on_getblocks)
        node.subscribe((Node.EVT_MESSAGE, MSG_GETHEADERS), self.on_getheaders)
        
        self.log = log
       
    def on_version_exchanged(self, event):
        self.log.info("blockchain server: version_exchanged")
    
    def on_disconnected(self, event):
        self.log.info("blockchain server: on_disconnected")
            
    def on_getdata(self, event):
        self.log.info("blockchain server: on_getdata")
        
    def on_getblocks(self, event):
        self.log.info("blockchain server: on_getblocks")
   
    def on_getheaders(self, event):
        self.log.info("blockchain server: on_getheaders")

