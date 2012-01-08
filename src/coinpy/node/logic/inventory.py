# -*- coding:utf-8 -*-
"""
Created on 7 Dec 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_INV
from coinpy.model.protocol.structures.invitem import INV_TX, INV_BLOCK, invitem
from coinpy.tools.observer import Observable
from coinpy.node.versionned_node import VersionnedNode
from coinpy.node.defines import MessageProcessed


class Inventory(Observable):
    EVT_NEW_HASHES = Observable.createevent()
    EVT_PEER_HEIGHT = Observable.createevent()
    
    def __init__(self, reactor, node, log):
        super(Inventory, self).__init__()
        node.add_handler((MSG_INV, INV_BLOCK), self.on_inv_block)
        node.add_handler((MSG_INV, INV_TX), self.on_inv_tx)
        
        self.log = log
        self.items = {} # { item => [peers, ...] , }
        
        self.new_txs = []
        self.new_blocks = []
        
        reactor.schedule_each(2, self.notify_newitems)
    
    def on_inv_tx(self, status, peer, hash):
        self.log.info("Inventory: on_inv_tx")
        isnew = (hash not in self.items)
        if isnew:
            self.items[hash] = []
        self.items[hash].append(peer)
        if isnew:
            self.new_txs.append(hash)
        status.processed()
        
    def on_inv_block(self, status, peer, hash):
        self.log.info("Inventory: on_inv_block")
      
        isnew = (hash not in self.items)
        if isnew:
            self.items[hash] = []
        self.items[hash].append(peer)
        if isnew:
            self.new_blocks.append(hash)
        status.processed()

    def search_item(self, item):
        if (item in self.items and len(self.items[item]) > 0):
            return (self.items[item][0])
        return (None)
    
    def notify_newitems(self):
        if (self.new_txs or self.new_blocks):
            items = [invitem(INV_TX, hash) for hash in self.new_txs] + \
                    [invitem(INV_BLOCK, hash) for hash in self.new_blocks]
            self.fire(Inventory.EVT_NEW_HASHES, items=items)
            self.new_txs = []
            self.new_blocks = []

