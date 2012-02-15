# -*- coding:utf-8 -*-
"""
Created on 13 Sep 2011

@author: kris
"""
from coinpy.model.protocol.structures.invitem import INV_BLOCK, INV_TX, invitem
from coinpy.model.protocol.messages.types import MSG_INV, MSG_TX, MSG_BLOCK
from coinpy.model.protocol.messages.getblocks import msg_getblocks
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.lib.bitcoin.hash_block import hash_block
from coinpy.model.protocol.messages.getdata import msg_getdata
from coinpy.lib.bitcoin.blockchain_with_pools import BlockchainWithPools
import traceback
from coinpy.node.version_exchange_node import VersionExchangeNode

class BlockchainDownloader():
    def __init__(self, reactor, blockchain_with_pools, node,log):
        self.blockchain_with_pools = blockchain_with_pools
        self.node = node

        self.log = log
        self.reactor = reactor
        
        node.add_handler((MSG_INV, INV_BLOCK), self.on_inv_block)
        node.add_handler((MSG_INV, INV_TX), self.on_inv_tx)
        node.add_handler(MSG_TX, self.on_tx)
        node.add_handler(MSG_BLOCK, self.on_block)
        
        self.node.subscribe (VersionExchangeNode.EVT_VERSION_EXCHANGED, self.on_version_exchange)
        self.blockchain_with_pools.subscribe (BlockchainWithPools.EVT_MISSING_BLOCK, self.on_missing_block)
        self.reactor.schedule_each(0.1, self.request_items)
        
        
        #self.items_to_download = []
        self.requested_tx = {}
        self.requested_blocks = {}
        
        self.required_items = {}
        self.firstrequest = True
        
    #1/keep up with peer heights in version exchanges    
    def on_version_exchange(self, event):
        peer_heigth = event.version_message.start_height
        my_height = self.blockchain_with_pools.blockchain.get_height()
        if (peer_heigth > my_height and self.firstrequest):
            locator = self.blockchain_with_pools.blockchain.get_block_locator()
            self.log.info("requesting blocks from %s, block locator: %s" % (str(event.handler.sockaddr), str(locator)))
            request = msg_getblocks(locator, uint256(0))
            self.node.send_message(event.handler, request)
            self.firstrequest = False
            
    #def on_item_downloaded(self, item):
    #   self.blockchain_with_pools.verified_add(item)


    def on_inv_tx(self, peer, item):
        #self.log.info("Inventory: on_inv_tx")
        if not self.blockchain_with_pools.has_transaction(item.hash):
            self.required_items.setdefault(peer, [])
            self.required_items[peer].append(item)
        
    def on_inv_block(self, peer, item):
        #self.log.info("Inventory: on_inv_block : %s" % (str(item)))
        if (self.blockchain_with_pools.is_orphan_block(item.hash)):
            self.push_getblocks(peer, item.hash)
        if not self.blockchain_with_pools.contains_block(item.hash):
            self.required_items.setdefault(peer, [])
            self.required_items[peer].append(item)
          
    def on_tx(self, peer, message):
        hash = hash_tx(message.tx)
        self.log.info("tx hash:%s" % (str(hash))) 
        if (hash not in self.requested_tx):
            #self.node.misbehaving(peer, "peer sending unrequest 'tx'")
            return
        self.requested_blocks[peer].remove(hash)
        self.blockchain_with_pools.verified_add_tx(message.tx)

    def push_getblocks(self, peer, end_hash):
        locator = self.blockchain_with_pools.blockchain.get_block_locator()
        #self.log.info("Sending Getblocks : %s" % (str(locator)))
        request = msg_getblocks(locator, end_hash)
        self.node.send_message(peer, request)
        
    def on_block(self, peer, message):
        hash = hash_block(message.block)
        #self.log.info("block : %s" % (str(hash)))
        if (hash not in self.requested_blocks[peer]):
            self.node.misbehaving(peer, "peer sending unrequest 'block' : %s" % hash)
            return
        #if (hash == ):
        #    pass
        self.requested_blocks[peer].remove(hash)
        self.blockchain_with_pools.add_block(peer, hash, message.block, self._blockadded_callback, (peer,))
        
    def _blockadded_callback(self, peer, error):
        if error:
            self.log.error(error)
            self.node.misbehaving(peer, str(error))
        #self.blockchain_with_pools.add_block(peer, hash, message.block)
        self.log.info("block added")
            
    def on_missing_block(self, event):
        self.push_getblocks(event.peer, event.missing_hash)
        
    def request_items(self):
        for peer, items in self.required_items.iteritems():
            #self.log.info("Downloading items %s" % (",".join((str(s) for s in items))))
            self.log.info("Downloading items: %d block, %d transactions" % (len([i for i in items if i.type == INV_BLOCK]), len([i for i in items if i.type == INV_TX])))
            
            #self.inprogress[item.hash] = (callback, callback_args)
            self.node.send_message(peer, msg_getdata(items))
            for item in items:
                if (item.type == INV_TX):
                    self.requested_tx.setdefault(peer, set()).add(item.hash)
                if (item.type == INV_BLOCK):
                    self.requested_blocks.setdefault(peer, set()).add(item.hash)
        self.required_items = {}


