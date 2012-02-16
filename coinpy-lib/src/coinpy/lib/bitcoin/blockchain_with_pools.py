# -*- coding:utf-8 -*-
"""
Created on 3 Jul 2011

@author: kris
"""
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.invitem import INV_TX, INV_BLOCK


from coinpy.lib.bitcoin.pools.blockpool import BlockPool

from coinpy.lib.bitcoin.checks.block_checks import BlockVerifier

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
        
    def verified_add_tx(self, item):
        self.log.info("Adding tx %s" % str(item))

    
    """
        Adds a block to the BlockchainWithPools
            returns: tuple(missing_blocks, errorneous_blocks)
    """
    def add_block(self, sender, hash, block, callback, args):
        if self.contains_block(hash):
            callback(*args, error =  Exception("Block allready added : %s" % (str(hash))))
            return
        #Checks-1 (done before finding the parent block) (main.cpp:1392)
        self.blockverifier.basic_checks(hash, block)
        #Find parent block in blockchain or declare orphan.
        if (not self.blockchain.contains_block(block.blockheader.hash_prev)):
            #Add to orphan blockpool
            self.orphanblocks.add_block(sender, hash, block)
            sender, missing_hash = self.orphanblocks.get_missing_root()
            self.fire(self.EVT_MISSING_BLOCK, peer=sender, missing_hash=missing_hash)
            callback(*args)
            return
        #Checks-2 (done after finding the parent block)
        #TODO: Check timestamp
        #if (GetBlockTime() > GetAdjustedTime() + 2 * 60 * 60)
        #return error("CheckBlock() : block timestamp too far in the future");       
        blockhandle = self.blockchain.appendblock(hash, block, self._appendblock_done, (callback, args))
        
    def _appendblock_done(self, callback, args, blockhandle=None, error=None):
        #if blockhandle.get_height() % 1 == 0:
        if not error:
            self.log.info("Appended block %d prev:%s, hash=%s" % (blockhandle.get_height(), str(blockhandle.get_blockheader().hash_prev), str(blockhandle.hash)))
        callback(*args, error=error)
        
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

