# -*- coding:utf-8 -*-
"""
Created on 13 Sep 2011

@author: kris
"""
from coinpy.model.protocol.structures.invitem import INV_BLOCK, Invitem
from coinpy.model.protocol.messages.types import MSG_INV, MSG_BLOCK
from coinpy.model.protocol.messages.getblocks import GetblocksMessage
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.lib.bitcoin.hash_block import hash_block
from coinpy.model.protocol.messages.getdata import GetdataMessage
import traceback
from coinpy.tools.reactor.asynch import asynch_method
from collections import deque
from coinpy.node.node import Node
from coinpy.node.logic.version_exchange import VersionExchangeService
from coinpy.model.protocol.messages.inv import InvMessage
from coinpy.lib.bitcoin.checks.block_checks import BlockVerifier
from coinpy.lib.bitcoin.pools.orphanblockpool import OrphanBlockPool

class BlockchainDownloader():
    # TODO: protect againts hosts that don't respond to GETDATA(timeout => misbehaving)
    # or don't respond to GETBLOCKS(much harder)
    def __init__(self, blockchain,  node, log):
        self.blockchain = blockchain
        self.node = node
        self.log = log
        
        self.requested_blocks = {}
        
        self.processing_block = False
        self.downloading = False
        self.sending_getblocks = False
        self.blocks_to_process = deque()
        self.getblock_to_send = deque()
        self.items_to_download = deque()
        self.firstrequest = True
        self.blockverifier = BlockVerifier(self.blockchain.database.runmode)
        self.orphanblocks =  OrphanBlockPool(log)
        
    def install(self, node):
        #assert VersionExchangeService is installed?
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_INV), self.on_inv)
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_BLOCK), self.on_block)
        
        self.node.subscribe (VersionExchangeService.EVT_VERSION_EXCHANGED, self.on_version_exchange)
        self.node.subscribe (Node.EVT_DISCONNECTED, self.on_peer_disconnected)
    

    #1/keep up with peer heights in version exchanges    
    def on_version_exchange(self, event):
        self.requested_blocks[event.handler] = set()
        peer_heigth = event.version_message.start_height
        my_height = self.blockchain.get_height()
        if (peer_heigth > my_height and self.firstrequest):
            self.push_getblocks(event.handler, Uint256.zero())
            self.firstrequest = False

    def on_inv(self, event):
        self.log.debug("on_inv")
        peer, message = event.handler, event.message
        items = []
        for item in message.items:
            if item.type == INV_BLOCK:
                if (self.orphanblocks.contains(item.hash)):
                    #after each geblocks, the other client sends an INV of the highest block 
                    #to continue download
                    self.push_getblocks(peer, item.hash)
                    #push_getblocks(peer, item.hash)
                else:
                    if (not self.blockchain.contains_block(item.hash) and 
                        not item.hash in self.requested_blocks):
                        items.append(item)
        if items:
            self.items_to_download.append([peer, items])
            
        if self.items_to_download:
            self._download_items()
        self.sending_getblocks = False

    def push_getblocks(self, peer, end_hash):
        self.getblock_to_send.append((peer, end_hash))
        if not self.processing_block:
            self._process_getblocks()
                    
    def _process_getblocks(self):
        self.sending_getblocks = True
        peer, end_hash = self.getblock_to_send.popleft()
        locator = self.blockchain.get_block_locator()
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
        if not self.requested_blocks[peer]:
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
                added_block_handles = yield self.accept_block(peer, hash, block)
                # relay blocks to peers
                for h in added_block_handles:
                    for p in self.node.version_service.version_exchanged_nodes:
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
        if peer in self.requested_blocks:
            self.requested_blocks[peer].clear()
        
    def on_peer_disconnected(self, event):
        self.cleanup_peer_tasks(event.handler)
        
    def _download_items(self):
        self.downloading = True
        #all blocks must be processed or INV continue might not find an orphan block
        peer, items = self.items_to_download.pop()
        self.log.info("Downloading items: %d block from %s: (%s...)" % 
                      (len([i for i in items if i.type == INV_BLOCK]), 
                       str(peer),
                       ",".join([str(i.hash) for i in items[:5]])))
            
        self.node.send_message(peer, GetdataMessage(items))
        for item in items:
            if (item.type == INV_BLOCK):
                self.requested_blocks[peer].add(item.hash)

    
    @asynch_method
    def accept_block(self, sender, hash, block):
        if hash in self.orphanblocks or self.blockchain.contains_block(hash):
            raise Exception("Block allready added : %s" % (str(hash)))
        #Checks-1 (done before finding the parent block) (main.cpp:1392)
        self.blockverifier.basic_checks(hash, block)
        #Find parent block in blockchain or declare orphan.
        if (not self.blockchain.contains_block(block.blockheader.hash_prev)):
            #Add to orphan blockpool
            self.log.info("Adding ophan block: %s" % (str( hash)))
            self.orphanblocks.add_block(sender, hash, block)
            sender, missing_hash = self.orphanblocks.get_orphan_root(hash)
            #request missing blocks from this peer
            if not self.getblock_to_send and not self.sending_getblocks:
                self.push_getblocks(sender, missing_hash)
            yield []
            return
        #TODO: Check timestamp
        #if (GetBlockTime() > GetAdjustedTime() + 2 * 60 * 60)
        #return error("CheckBlock() : block timestamp too far in the future");     
        block_handle = yield self.add_to_blockchain(hash, block)
        added_block_handles = [block_handle]
        #recursively process any orphan blocks that depended on this one
        descendent_blocks = self.orphanblocks.pop_descendant_blocks(hash)
        for sender, blkhash, block in descendent_blocks:
            block_handle = yield self.add_to_blockchain(blkhash, block)
            added_block_handles.append(block_handle)
        yield added_block_handles

    @asynch_method
    def add_to_blockchain(self, blkhash, block):
        #Checks-2 (done after finding the parent block)
        self.blockverifier.accept_block(blkhash, block, self.blockchain)
        yield self.blockchain.appendblock(blkhash, block)
