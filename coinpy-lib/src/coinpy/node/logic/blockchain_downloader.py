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
from coinpy.tools.reactor.asynch import Asynch, asynch_method
import time
from collections import deque

class BlockchainDownloader():
    # TODO: protect againts hosts that don't respond to GETDATA(timeout => misbehaving)
    # or don't respond to GETBLOCKS(much harder)
    def __init__(self, reactor, blockchain_with_pools, node, log):
        self.blockchain_with_pools = blockchain_with_pools
        self.node = node

        self.log = log
        self.reactor = reactor
        
        node.subscribe((node.EVT_MESSAGE, MSG_INV), self.on_inv)
        node.subscribe((node.EVT_MESSAGE, MSG_TX), self.on_tx)
        node.subscribe((node.EVT_MESSAGE, MSG_BLOCK), self.on_block)
        
        self.node.subscribe (VersionExchangeNode.EVT_VERSION_EXCHANGED, self.on_version_exchange)
        self.blockchain_with_pools.subscribe (BlockchainWithPools.EVT_MISSING_BLOCK, self.on_missing_block)
        
        self.requested_tx = set()
        self.requested_blocks = set()
        
        self.blocks_to_process = deque()
        self.processing_block = False
        self.downloading = False
        self.items_to_download = deque()
        self.firstrequest = True
        self.getblock_to_send = deque()
        
    #1/keep up with peer heights in version exchanges    
    def on_version_exchange(self, event):
        peer_heigth = event.version_message.start_height
        my_height = self.blockchain_with_pools.blockchain.get_height()
        if (peer_heigth > my_height and self.firstrequest):
            self.push_getblocks(event.handler, uint256.zero())
            self.firstrequest = False

    """def on_inv(self, peer, item):
        if not self.blockchain_with_pools.contains_transaction(item.hash):
            self.required_items.setdefault(peer, [])
            self.required_items[peer].append(item)
    """   
    def on_inv(self, event):
        self.log.debug("on_inv")
        peer, message = event.handler, event.message
        items = []
        for item in message.items:
            if item.type == INV_TX:
                if not self.blockchain_with_pools.contains_transaction(item.hash):
                    items.append(item)
            if item.type == INV_BLOCK:
                if (self.blockchain_with_pools.is_orphan_block(item.hash)):
                    #after each geblocks, the other client sends an INV of the highest block 
                    #to continue download
                    self.push_getblocks(peer, item.hash)
                    #push_getblocks(peer, item.hash)
                if not self.blockchain_with_pools.contains_block(item.hash):
                    items.append(item)
        if items:
            self.items_to_download.append([peer, items])
            
        if self.items_to_download:
            self._download_items()
          
    def on_tx(self, event):
        peer, message = event.handler, event.message
        hash = hash_tx(message.tx)
        self.log.debug("on_tx hash:%s" % (str(hash))) 
        if (hash not in self.requested_tx):
            #self.node.misbehaving(peer, "peer sending unrequest 'tx'")
            return
        self.requested_tx.remove(hash)
        if not self.requested_blocks and not self.requested_tx:
            self.downloading = False
        self.blockchain_with_pools.verified_add_tx(message.tx)

    def push_getblocks(self, peer, end_hash):
        self.getblock_to_send.append((peer, end_hash))
        if not self.processing_block:
            self._process_getblocks()
                    
    def _process_getblocks(self):
        peer, end_hash = self.getblock_to_send.popleft()
        locator = self.blockchain_with_pools.blockchain.get_block_locator()
        self.log.info("requesting blocks from %s, block locator: %s" % (str(peer), str(locator)))
        request = msg_getblocks(locator, end_hash)
        self.node.send_message(peer, request)
        
    def on_block(self, event):
        self.log.debug("on_block")
        peer, message = event.handler, event.message
        hash = hash_block(message.block)
        #self.log.info("block : %s" % (str(hash)))
        if (hash not in self.requested_blocks):
            self.node.misbehaving(peer, "peer sending unrequest 'block' : %s" % hash)
            return
        self.requested_blocks.remove(hash)
        if not self.requested_blocks and not self.requested_tx:
            self.downloading = False
        self.blocks_to_process.append( (peer, hash, message.block))
        self.start_processing()

    def on_missing_block(self, event):
        self.push_getblocks(event.peer, event.missing_hash)
    
    def start_processing(self):
        if not self.processing_block:
            self.log.debug("start_processing")
            self.processing_block = True
            self.reactor.call_asynch(self._process_blocks())

    @asynch_method
    def _process_blocks(self):
        while self.blocks_to_process:
            peer, hash, block = self.blocks_to_process.popleft()
            self.log.debug("processing block : %s" % (hash))
            try:
                yield self.blockchain_with_pools.add_block(peer, hash, block)
            except Exception as e:
                self.node.misbehaving(peer, str(e))
                return
        self.processing_block = False
        self.log.debug("end_processing")
            
        if self.items_to_download:
            self._download_items()
        if self.getblock_to_send:
            self._process_getblocks()
            
    def _download_items(self):
        self.downloading = True
        #all blocks must be processed or INV continue might not find an orphan block
        peer, items = self.items_to_download.pop()
        self.log.info("Downloading items: %d block, %d transactions from %s" % (len([i for i in items if i.type == INV_BLOCK]), len([i for i in items if i.type == INV_TX]), str(peer)))
            
        self.node.send_message(peer, msg_getdata(items))
        for item in items:
            if (item.type == INV_TX):
                self.requested_tx.add(item.hash)
            if (item.type == INV_BLOCK):
                self.requested_blocks.add(item.hash)

