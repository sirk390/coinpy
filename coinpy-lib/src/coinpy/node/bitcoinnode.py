# -*- coding:utf-8 -*-
"""
Created on 17 Sep 2011

@author: kris
"""
from coinpy.node.node import Node
from coinpy.node.logic.blockchain_server import BlockchainServer
from coinpy.node.logic.blockchain_downloader import BlockchainDownloader
from coinpy.model.protocol.messages.types import MESSAGE_TYPES
from coinpy.node.message_dispatcher_node import MessageDispatcherNode

class BitcoinNode(MessageDispatcherNode):
    def __init__(self, reactor, blockchain_with_pools, params, log):
        super(BitcoinNode, self).__init__(reactor, lambda : 0, params, log)
         
        #self.inventory = Inventory(reactor, self, log) # handle inv, startheight
        #self.itemdownloader = ItemDownloader(reactor, self, self.inventory, log) # send getdata, handle tx, block messages
        #self.blockfinder = BlockFinder(reactor, self, self.itemdownloader, blockchain_with_pools.blockchain, log) # send getblocks, handle inv 
        
        self.blockchain_downloader = BlockchainDownloader(reactor, blockchain_with_pools, self, self.log)
     

