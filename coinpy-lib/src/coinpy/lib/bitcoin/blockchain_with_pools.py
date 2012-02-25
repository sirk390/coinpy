# -*- coding:utf-8 -*-
"""
Created on 3 Jul 2011

@author: kris
"""
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.invitem import INV_TX, INV_BLOCK


from coinpy.lib.bitcoin.pools.blockpool import BlockPool

from coinpy.lib.bitcoin.checks.block_checks import BlockVerifier
from coinpy.tools.reactor.asynch import asynch_method
from collections import deque

class BlockchainWithPools(Observable):
    EVT_MISSING_BLOCK = Observable.createevent()
    
    def __init__(self, 
                 blockchain, 
                 log,
                 orphantransactions = set(),
                 transactionpool = set()):
        super(BlockchainWithPools, self).__init__()
        self.blockchain = blockchain
        self.orphanblocks =  BlockPool(log)
        self.orphantransactions = orphantransactions
        self.transactionpool = transactionpool
        self.log = log
        self.runmode = self.blockchain.database.runmode
        
        self.blockverifier = BlockVerifier(self.runmode)
        
        self.add_blockchain_queue = deque()
        
    def verified_add_tx(self, item):
        self.log.info("Adding tx %s" % str(item))

    
    """
        Asynch method: send to reactor.call_asych( )
        Adds a block to the BlockchainWithPools
    """
    @asynch_method
    def add_block(self, sender, hash, block):
        if self.contains_block(hash):
            raise Exception("Block allready added : %s" % (str(hash)))
        #Checks-1 (done before finding the parent block) (main.cpp:1392)
        self.blockverifier.basic_checks(hash, block)
        #Find parent block in blockchain or declare orphan.
        if (not self.blockchain.contains_block(block.blockheader.hash_prev)):
            #Add to orphan blockpool
            self.orphanblocks.add_block(sender, hash, block)
            sender, missing_hash = self.orphanblocks.get_missing_root()
            self.fire(self.EVT_MISSING_BLOCK, peer=sender, missing_hash=missing_hash)
            return
        #Checks-2 (done after finding the parent block)
        #TODO: Check timestamp
        #if (GetBlockTime() > GetAdjustedTime() + 2 * 60 * 60)
        #return error("CheckBlock() : block timestamp too far in the future");     
        yield self.blockchain.appendblock(hash, block)
        #self.log.info("Appended block %d prev:%s, hash=%s" % (blockhandle.get_height(), str(blockhandle.get_blockheader().hash_prev), str(blockhandle.hash)))
        
    def contains_transaction(self, hash):
        return (self.blockchain.contains_transaction(hash) or 
                hash in self.transactionpool or 
                hash in self.orphantransactions)

    def contains_block(self, hash):
        return (self.blockchain.contains_block(hash) or 
                hash in self.orphanblocks)
        
    def is_orphan_block(self, hash):
        return (hash in self.orphanblocks)

    def has_item(self, item):
        if (item.type == INV_TX):
            return (self.has_transaction(item.hash))
        if (item.type == INV_BLOCK):
            return (self.has_block(item.hash))
        raise ("Unkwnow item type")
