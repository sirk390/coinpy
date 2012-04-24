# -*- coding:utf-8 -*-
"""
Created on 3 Jul 2011

@author: kris
"""
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.invitem import INV_TX, INV_BLOCK
from coinpy.lib.bitcoin.pools.orphanblockpool import OrphanBlockPool
from coinpy.lib.bitcoin.checks.block_checks import BlockVerifier
from coinpy.tools.reactor.asynch import asynch_method
from collections import deque
from coinpy.lib.bitcoin.hash_tx import hash_tx

class BlockchainWithPools(Observable):
    EVT_MISSING_BLOCK = Observable.createevent()
    EVT_ADDED_ORPHAN_TX = Observable.createevent()
    EVT_REMOVED_ORPHAN_TX = Observable.createevent()
    EVT_ADDED_ORPHAN_BLOCK = Observable.createevent()
    EVT_REMOVED_ORPHAN_BLOCK = Observable.createevent()
    EVT_ADDED_TX = Observable.createevent()
    EVT_REMOVED_TX = Observable.createevent()
    
    def __init__(self, 
                 blockchain, 
                 log,
                 orphantransactions = {},
                 transactionpool = {}):
        super(BlockchainWithPools, self).__init__()
        self.blockchain = blockchain
        self.orphanblocks =  OrphanBlockPool(log)
        self.orphantransactions = orphantransactions
        self.transactionpool = transactionpool
        self.log = log
        self.runmode = self.blockchain.database.runmode
        
        self.blockverifier = BlockVerifier(self.runmode)
        
        self.add_blockchain_queue = deque()
        
    def verified_add_tx(self, tx):
        self.fire(self.EVT_ADDED_TX, hash = hash_tx(tx))
        self.log.info("Adding tx %s" % str(tx))
    
    def add_transaction(self, txhash, tx):
        self.fire(self.EVT_ADDED_TX, hash=txhash)
        self.transactionpool[txhash] = tx
    
    @asynch_method
    def add_block(self, sender, hash, block):
        if self.contains_block(hash):
            raise Exception("Block allready added : %s" % (str(hash)))
        #Checks-1 (done before finding the parent block) (main.cpp:1392)
        self.blockverifier.basic_checks(hash, block)
        #Find parent block in blockchain or declare orphan.
        if (not self.blockchain.contains_block(block.blockheader.hash_prev)):
            #Add to orphan blockpool
            self.log.info("Adding ophan block: %s" % (str( hash)))
            self.orphanblocks.add_block(sender, hash, block)
            sender, missing_hash = self.orphanblocks.get_orphan_root(hash)
            self.fire(self.EVT_MISSING_BLOCK, peer=sender, missing_hash=missing_hash)
            self.fire(self.EVT_ADDED_ORPHAN_BLOCK, hash=hash)
            return
        #Checks-2 (done after finding the parent block)
        self.blockverifier.accept_block(hash, block, self.blockchain)
        
        #TODO: Check timestamp
        #if (GetBlockTime() > GetAdjustedTime() + 2 * 60 * 60)
        #return error("CheckBlock() : block timestamp too far in the future");     
        yield self.blockchain.appendblock(hash, block)
        
        #recursively process any orphan blocks that depended on this one
        descendent_blocks = self.orphanblocks.pop_descendant_blocks(hash)
        for sender, blkhash, block in descendent_blocks:
            self.fire(self.EVT_REMOVED_ORPHAN_TX, hash=blkhash)
        for sender, blkhash, block in descendent_blocks:
            self.blockverifier.accept_block(blkhash, block, self.blockchain)
            yield self.blockchain.appendblock(blkhash, block)
            
        
    def get_transaction(self, hash):
        if hash in self.transactionpool:
            return self.transactionpool[hash]
        if hash in self.orphantransactions:
            return self.orphantransactions[hash]
        if self.blockchain.contains_transaction(hash):
            return self.blockchain.get_transaction_handle(hash).get_transaction()
        return None
        
    def contains_transaction(self, hash):
        return (self.blockchain.contains_transaction(hash) or 
                hash in self.transactionpool or 
                hash in self.orphantransactions)

    def contains_block(self, hash):
        return (self.blockchain.contains_block(hash) or 
                hash in self.orphanblocks)
        
    def get_block(self, blkhash):
        if blkhash in self.orphanblocks:
            return self.orphanblocks.get_block(blkhash)
        if self.blockchain.contains_block(blkhash):
            return self.blockchain.get_block(blkhash)
        return None
        
    def is_orphan_block(self, hash):
        return (hash in self.orphanblocks)

    def has_item(self, item):
        if (item.type == INV_TX):
            return (self.has_transaction(item.hash))
        if (item.type == INV_BLOCK):
            return (self.has_block(item.hash))
        raise ("Unkwnow item type")

