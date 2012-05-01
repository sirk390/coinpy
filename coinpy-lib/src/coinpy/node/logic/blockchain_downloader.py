# -*- coding:utf-8 -*-
"""
Created on 13 Sep 2011

@author: kris
"""
from coinpy.model.protocol.structures.invitem import INV_BLOCK, INV_TX, Invitem
from coinpy.model.protocol.messages.types import MSG_INV, MSG_TX, MSG_BLOCK
from coinpy.model.protocol.messages.getblocks import GetblocksMessage
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.lib.bitcoin.hash_block import hash_block
from coinpy.model.protocol.messages.getdata import GetdataMessage
from coinpy.lib.bitcoin.blockchain_with_pools import BlockchainWithPools
import traceback
from coinpy.tools.reactor.asynch import asynch_method
from collections import deque
from coinpy.node.node import Node
from coinpy.node.logic.version_exchange import VersionExchangeService
from coinpy.model.protocol.messages.inv import InvMessage

class BlockchainDownloader():
    # TODO: protect againts hosts that don't respond to GETDATA(timeout => misbehaving)
    # or don't respond to GETBLOCKS(much harder)
    def __init__(self, blockchain_with_pools, node, log):
        self.blockchain_with_pools = blockchain_with_pools
        self.node = node

        self.log = log
        
        
        self.requested_tx = {}
        self.requested_blocks = {}
        
        self.processing_block = False
        self.downloading = False
        self.sending_getblocks = False
        self.blocks_to_process = deque()
        self.getblock_to_send = deque()
        self.items_to_download = deque()
        self.firstrequest = True
        
    def install(self, node):
        #assert VersionExchangeService is installed?
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_INV), self.on_inv)
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_TX), self.on_tx)
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_BLOCK), self.on_block)
        
        self.blockchain_with_pools.subscribe (BlockchainWithPools.EVT_MISSING_BLOCK, self.on_missing_block)
        self.node.subscribe (VersionExchangeService.EVT_VERSION_EXCHANGED, self.on_version_exchange)
        self.node.subscribe (Node.EVT_DISCONNECTED, self.on_peer_disconnected)
    

    #1/keep up with peer heights in version exchanges    
    def on_version_exchange(self, event):
        self.requested_tx[event.handler] = set()
        self.requested_blocks[event.handler] = set()
        peer_heigth = event.version_message.start_height
        my_height = self.blockchain_with_pools.blockchain.get_height()
        if (peer_heigth > my_height and self.firstrequest):
            self.push_getblocks(event.handler, Uint256.zero())
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
        self.sending_getblocks = False
         
    def on_tx(self, event):
        peer, message = event.handler, event.message
        hash = hash_tx(message.tx)
        self.log.debug("on_tx hash:%s" % (str(hash))) 
        if (hash not in self.requested_tx[peer]):
            #self.node.misbehaving(peer, "peer sending unrequest 'tx'")
            return
        self.requested_tx[peer].remove(hash)
        if not self.requested_blocks[peer] and not self.requested_tx[peer]:
            self.downloading = False
        self.blockchain_with_pools.verified_add_tx(message.tx)

    def push_getblocks(self, peer, end_hash):
        self.getblock_to_send.append((peer, end_hash))
        if not self.processing_block:
            self._process_getblocks()
                    
    def _process_getblocks(self):
        self.sending_getblocks = True
        peer, end_hash = self.getblock_to_send.popleft()
        locator = self.blockchain_with_pools.blockchain.get_block_locator()
        self.log.info("requesting blocks from %s, block locator: %s" % (str(peer), str(locator)))
        request = GetblocksMessage(locator, end_hash)
        self.node.send_message(peer, request)
        
    def on_block(self, event):
        peer, message = event.handler, event.message
        hash = hash_block(message.block)
        self.log.debug("on_block : %s" % (str(hash)))
        if (hash not in self.requested_blocks[peer]):
            #self.node.misbehaving(peer, "peer sending unrequest 'block' : %s" % hash)
            self.misbehaving(peer, "peer sending unrequest 'block' : %s" % hash)
            return
        self.requested_blocks[peer].remove(hash)
        if not self.requested_blocks[peer] and not self.requested_tx[peer]:
            self.downloading = False
        self.blocks_to_process.append( (peer, hash, message.block))
        self.start_processing()

    def on_missing_block(self, event):
        if not self.getblock_to_send and not self.sending_getblocks:
            self.push_getblocks(event.peer, event.missing_hash)
    
    def start_processing(self):
        if not self.processing_block:
            self.log.debug("start_processing")
            self.processing_block = True
            self._process_blocks()

    @asynch_method
    def _process_blocks(self):
        while self.blocks_to_process:
            peer, hash, block = self.blocks_to_process.popleft()
            self.log.debug("processing block : %s" % (hash))
            try:
                added_block_handles = yield self.blockchain_with_pools.add_block(peer, hash, block)
                # relay blocks to peers
                for h in added_block_handles:
                    for p in self.node.connection_manager.connected_peers:
                        if h.get_height() > self.node.version_service.version_statuses[p].version_message.start_height - 2000:
                            self.node.send_message(peer, InvMessage([Invitem(INV_BLOCK, h.hash)]))
            except Exception as e:
                self.log.error(traceback.format_exc())
                self.misbehaving(peer, str(e))
                return
        self.processing_block = False
        self.log.debug("end_processing")
            
        if self.items_to_download:
            self._download_items()
        if self.getblock_to_send:
            self._process_getblocks()
    
    def misbehaving(self, peer, reason):
        self.cleanup_peer_tasks()
        self.node.misbehaving(peer, reason)

    def cleanup_peer_tasks(self, peer):
        self.blocks_to_process = deque(filter(lambda (p, hash, blk): p != peer, self.blocks_to_process))
        self.getblock_to_send = deque(filter(lambda (p, end_hash): p != peer, self.getblock_to_send))        
        self.items_to_download = deque(filter(lambda (p, items): p != peer, self.items_to_download))   
        if peer in self.requested_tx:
            self.requested_tx[peer].clear()
        if peer in self.requested_blocks:
            self.requested_blocks[peer].clear()
        
    def on_peer_disconnected(self, event):
        self.cleanup_peer_tasks(event.handler)
        
    def _download_items(self):
        self.downloading = True
        #all blocks must be processed or INV continue might not find an orphan block
        peer, items = self.items_to_download.pop()
        self.log.info("Downloading items: %d block, %d transactions from %s: (%s...)" % 
                      (len([i for i in items if i.type == INV_BLOCK]), 
                       len([i for i in items if i.type == INV_TX]), 
                       str(peer),
                       ",".join([str(i.hash) for i in items[:5]])))
            
        self.node.send_message(peer, GetdataMessage(items))
        for item in items:
            if (item.type == INV_TX):
                self.requested_tx[peer].add(item.hash)
            if (item.type == INV_BLOCK):
                self.requested_blocks[peer].add(item.hash)

