# -*- coding:utf-8 -*-
"""
Created on 13 Sep 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_GETDATA, MSG_GETBLOCKS,\
    MSG_GETHEADERS
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.invitem import INV_TX, INV_BLOCK, Invitem
from coinpy.model.protocol.messages.tx import TxMessage
from coinpy.tools.functools import first
from coinpy.model.protocol.messages.block import BlockMessage
from coinpy.model.protocol.messages.inv import InvMessage
from coinpy.node.logic.version_exchange import VersionExchangeService


class BlockchainServer(Observable):
    def __init__(self, reactor, node, blockchain_with_pools, log):
        super(BlockchainServer, self).__init__(reactor)
        self.blockchain_with_pools = blockchain_with_pools
        self.blockchain = blockchain_with_pools.blockchain
        self.node = node
        self.log = log
        self.hash_continue = None

    def install(self, node):
        node.subscribe(VersionExchangeService.EVT_VERSION_EXCHANGED, self.on_version_exchanged)      
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_GETDATA), self.on_getdata)
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_GETBLOCKS), self.on_getblocks)
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_GETHEADERS), self.on_getheaders)
        
    def on_version_exchanged(self, event):
        pass
    
    def on_disconnected(self, event):
        pass
            
    def on_getdata(self, event):
        for inv in event.message.invitems:
            if inv.type == INV_TX and self.blockchain_with_pools.contains_transaction(inv.hash):
                tx = self.blockchain_with_pools.get_transaction(inv.hash)
                self.node.send_message(event.handler, TxMessage(tx))
            if inv.type == INV_BLOCK and self.blockchain_with_pools.contains_block(inv.hash):
                block = self.blockchain_with_pools.get_block(inv.hash)
                self.node.send_message(event.handler, BlockMessage(block))
                if self.hash_continue and inv.hash == self.hash_continue:
                    hash_best = self.blockchain.database.get_mainchain()
                    self.log.info("sending hashContinue: %s" % (str(hash_best)))
                    self.node.send_message(event.handler, InvMessage([Invitem(INV_BLOCK, hash_best)]))
                
    def on_getblocks(self, event):
        firstfound = first(event.message.block_locator.blockhashlist, 
                           lambda b: self.blockchain.contains_block(b))
        blkhash, i =  firstfound, 0
        inv_to_send = []
        while blkhash and blkhash != event.message.hash_stop and i < 500:
            blkhash = self.blockchain.get_next_in_mainchain(blkhash)
            if blkhash:
                inv_to_send.append(Invitem(INV_BLOCK, blkhash))
            i += 1
        self.node.send_message(event.handler, InvMessage(inv_to_send))
        self.hash_continue = blkhash 
        self.log.info("sending reply to getblocks: %d items" % (len(inv_to_send)))
   
    def on_getheaders(self, event):
        self.log.info("blockchain server: on_getheaders")

