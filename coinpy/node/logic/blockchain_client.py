# -*- coding:utf-8 -*-
"""
Created on 13 Sep 2011

@author: kris
"""
from coinpy.node.versionned_node import VersionnedNode
from coinpy.model.protocol.messages.types import MSG_GETDATA, MSG_GETBLOCKS,\
    MSG_GETHEADERS, MSG_INV, MSG_TX, MSG_BLOCK, MSG_HEADERS
from coinpy.node.node import Node
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.invitem import INV_TX, INV_BLOCK, invitem
from IPython.Extensions.ipipe import deque
import time
from coinpy.tools.functools import xgroupby
from coinpy.model.protocol.messages.getdata import msg_getdata
from coinpy.node.logic.status.download_status import DownloadStatus
from coinpy.lib.hash.hash_tx import hash_tx
from coinpy.node.logic.status.getblocks_request import GetBlocksRequest
from coinpy.model.protocol.messages.getblocks import msg_getblocks
from coinpy.node.logic.status.getdata_tx_handler import GetdataTXHandler

class BlockchainClient(Observable):
    CALLBACK_TYPES = INV_TX, CB_INV_BLOCK, CB_TX, CB_BLOCK = range(4), 
    
    def __init__(self, node, log):
        super(BlockchainClient, self).__init__()
        
        self.node = node
        node.subscribe(VersionnedNode.EVT_VERSION_EXCHANGED, self.on_version_exchanged)     
        node.subscribe(Node.EVT_DISCONNECTED, self.on_disconnected)
        
        node.subscribe((MSG_INV, self.on_inv))
        node.subscribe((MSG_TX, self.on_tx))
        node.subscribe((MSG_BLOCK, self.on_block))
        node.subscribe((MSG_HEADERS, self.on_headers))
        
        self.callbacks = dict((type, []) for type in self.CALLBACK_TYPES)
        
    def on_version_exchanged(self, event):
        #event.version_message.start_height
        self.log.info("Version_exchanged with node of height: %d" % (event.version_message.start_height))
        self.startheights[event.handler] = event.version_message.start_height
        self.download_statuses[event.handler] = DownloadStatus()
        
    def on_disconnected(self, event):
        self.log.info("blockchain downloader: disconnected")
        if event.handler in self.startheights:
            del self.startheights[event.handler]

    def on_inv(self, event):
        for item in event.message.items:
            if (item.type == INV_TX):
                self.incoming_tx.append((event.peer,item.hash))
            elif (item.type == INV_BLOCK):
                self.incoming_blocks.append((event.peer,item.hash))
            else:
                self.node.report_peer(event.peer, "peer sent invalid item type: %d" % (item.type))
        
    def on_tx(self, event):
        pass
    
    def on_block(self, event):
        pass
        
    def on_headers(self, event):
        self.log.info("blockchain downloader: headers")

    # getdata, getblocks
    def add_getdata_request(self, request):
        pass
        #getdata = GetDataRequest()
        #self.getdata_request.append()
        #return (getdata)



