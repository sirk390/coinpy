# -*- coding:utf-8 -*-
"""
Created on 7 Dec 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_TX, MSG_BLOCK, MSG_INV
from coinpy.lib.hash.hash_tx import hash_tx
from coinpy.lib.hash.hash_block import hash_block
from coinpy.model.protocol.messages.getdata import msg_getdata
from coinpy.node.defines import MessageProcessed, MessageUnprocessed
from coinpy.model.protocol.structures.invitem import INV_BLOCK, INV_TX

class ItemDownloader():
    def __init__(self, reactor, node, inventory, log):
        node.add_handler((MSG_INV, INV_BLOCK), self.on_inv_block)
        node.add_handler((MSG_INV, INV_TX), self.on_inv_tx)
        node.add_handler(MSG_TX, self.on_tx)
        node.add_handler(MSG_BLOCK, self.on_block)
        self.log = log
        self.node = node
        self.reactor = reactor
        
        self.items_to_download = []
        self.inprogress = {}
        
        reactor.schedule_each(1, self.download_items)

    def on_inv_tx(self, status, peer, hash):
        self.log.info("Inventory: on_inv_tx")
        
    def on_inv_block(self, status, peer, hash):
        self.log.info("Inventory: on_inv_block")
         
    def request_download(self, item, callback, *callback_args):
        peer = self.inventory.search_item(item)
        if (peer):
            self.items_to_download.append((peer, item, callback, callback_args))
        else:
            self.log.warning("Can't find peer for element %s" % str(item))       
        
    def request_download_from_peer(self, peer, item, callback, *callback_args):
        self.items_to_download.append((peer, item, callback, callback_args))
 
    def on_tx(self, status, event):
        hash = hash_tx(event.message.tx)
        self.log.info("tx hash:%s, inprogress:%s" % (str(hash), str(self.inprogress.keys()[0])) )
        if (hash not in self.inprogress):
            self.node.misbehaving(event.handler, "peer sending unrequest 'tx'")
            status.processed()
        callback, callback_args = self.inprogress[hash] 
        if callback:
            self.reactor.call(callback, event.message.tx)
        del self.inprogress[hash]
        status.processed()
        
    def on_block(self, status, event):
        hash = hash_block(event.message.block)
        if (hash not in self.inprogress):
            return
            #unrequested block (leave it for the default handler)
            #status.processed()
        callback, callback_args = self.inprogress[hash] 
        if callback:
            self.reactor.call(callback, event.message.block, *callback_args)
        del self.inprogress[hash]
        status.processed()
    
    def download_items(self):
        for peer, item, callback, callback_args in self.items_to_download:
            self.log.info("Downloading %s" % str(item))
            
            self.inprogress[item.hash] = (callback, callback_args)
            self.node.send_message(peer, msg_getdata([item]))
           
        self.items_to_download = []

