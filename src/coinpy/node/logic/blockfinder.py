# -*- coding:utf-8 -*-
"""
Created on 7 Dec 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_INV
from coinpy.model.protocol.structures.invitem import INV_TX, INV_BLOCK, invitem
from coinpy.tools.observer import Observable
from coinpy.model.protocol.messages.getblocks import msg_getblocks
from coinpy.node.defines import MessageProcessed, MessageUnprocessed
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.bitcoin.hash_block import hash_block


class BlockFinder(Observable):
    EVT_NEW_ITEMS = Observable.createevent()
    """    
        blockchain: required to verify the height of returned blocks
    """
    def __init__(self, reactor, node, itemdownloader, blockchain, log):
        node.add_handler((MSG_INV, INV_BLOCK), self.on_inv_block, 1)
        self.reactor = reactor
        self.node = node
        self.blockchain = blockchain
        self.itemdownloader = itemdownloader
        self.log = log

        self.getblocks_in_progress = None
        self.blocks_to_download = []
        self.downloaded_blocks = {}
        
        self.parented_lists = {} # {hash_last => [(hash, block), (hash, block), ...] , ...}
        self.common_parent = None
        reactor.schedule_each(1, self.download_blocks)
        
        self.height = None
        self.peer_height = None
        
    def search_blocks(self, peer, block_locator, height, peer_height, callback):
        if (self.getblocks_in_progress):
            raise Exception("getblocks allready in progress")
        self.expected_results = 500
        self.height = height
        self.peer = peer
        self.peer_height = peer_height
        request = msg_getblocks(self.node.params.version, block_locator, uint256(0))
        self.getblocks_in_progress = request
        #self.downloaded_blocks = {}
        self.blocks_to_download = []
        #self.parented_lists = {}
        self.blockpool = BlockPool(self.log)
        self.node.send_message(peer, request)
        
    def on_inv_block(self, status, peer, hash):
        #self.log.info("BlockFinder: on_inv_block")
        if (self.getblocks_in_progress and peer == self.peer):
            #possible result of a getblocks request, or maybe a new unrequested block
            self.blocks_to_download.append(hash)
            status.inprogress()
         
    def download_blocks(self):
        for hash in self.blocks_to_download:
            self.itemdownloader.request_download_from_peer(self.peer, invitem(INV_BLOCK, hash), self.on_block_downloaded, hash)
        self.blocks_to_download = []
        
    def is_in_progress(self):
        return self.getblocks_in_progress
    
    def on_block_downloaded(self, block, hash):
        if (not self.common_parent): 
            parentref = self.blockchain.getblockref(block.blockheader.hash_prev)
            self.expected_results = min(self.peer_height - parentref.height(), self.expected_results)
            self.log.info("found first chain parent for block: %s, height:%d, expected results:%d" % (str(hash), parentref.height(), self.expected_results))
            self.common_parent = (hash, block, parentref)
        self.blockpool.add_block(hash, block)
      
        if (self.common_parent):
            hash, block, parentref = self.common_parent 
            if (len(self.blockpool.previndex[block.blockheader.hash_prev]) == self.expected_results):
                self.log.info("downloaded all expected blocks (done:%d, to_dl:%d)" % (len(self.downloaded_blocks), len(self.blocks_to_download))) 
                #self.blockchain.add_verify_blocks(self.blockpool.previndex[block.blockheader.hash_prev])
                #verify blocks, mark all status as ok, release other statuses
                
                #exit(0)
        #hash = hash_block(block)
        #self.log.info("block downloaded : %s" % str(hash))
        
