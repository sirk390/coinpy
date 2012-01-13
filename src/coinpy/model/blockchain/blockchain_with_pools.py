# -*- coding:utf-8 -*-
"""
Created on 3 Jul 2011

@author: kris
"""
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.invitem import INV_TX, INV_BLOCK


from coinpy.lib.serialization.messages.s11n_tx import tx_encoder
from coinpy.tools.hex import hexdump, hexstr
from coinpy.model.blockchain.blockpool import BlockPool
from coinpy.model.constants.bitcoin import TARGET_INTERVAL, MEDIAN_TIME_SPAN
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.model.blockchain.checkpoints import verify_checkpoints,\
    get_checkpoint
from coinpy.lib.bitcoin.blockverifier import BlockVerifier

class BlockchainWithPools(Observable):
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
        self.runmode = self.blockchain.runmode
        
        self.blockverifier = BlockVerifier(self.runmode)
        
    def verified_add_tx(self, item):
        self.log.info("Adding tx %s" % str(item))
    
    """
        Adds a block to the BlockchainWithPools
            returns: tuple(missing_blocks, errorneous_blocks)
    """
    def add_block(self, sender, hash, block):
        missing_blocks, incorrect_blocks = [], []
        #Checks-1 (done before finding the parent block) (main.cpp:1392)
        result = self.blockverifier.basic_checks(hash, block)
        if (result):
            return ([], [(sender, block, "error in basic checks:" + result.message)])
        #Find parent block in blockchain or declare orphan.
        if (not self.blockchain.contains_block(block.blockheader.hash_prev)):
            #Add to orphan blockpool
            self.orphanblocks.add_block(sender, hash, block)
            return ([self.orphanblocks.get_missing_root()], [])
        #Checks-2 (done after finding the parent block)
        result = self.blockverifier.accept_block(hash, block, self.blockchain)
        if (result):
            return ([], [(sender, block, "error in block:" + result.message)])
        #TODO: Check timestamp
        #if (GetBlockTime() > GetAdjustedTime() + 2 * 60 * 60)
        #return error("CheckBlock() : block timestamp too far in the future");

        
        #TODO: check transactions
        
        #TODO:relay
        #add it to the blockchain
        self.blockchain.appendblock(hash, block)
        return ([], [])
    
    def has_transaction(self, hash):
        return (self.blockchain.contains_transaction(hash) or 
                hash in self.transactionpool or 
                hash in self.orphantransactions)

    def has_block(self, hash):
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

