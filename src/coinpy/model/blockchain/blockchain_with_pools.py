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
        
        result = self.blockverifier.basic_check(hash, block)
        if (result):
            return ([], [(sender, block, "error in basic checks:" + result.message)])
        
        #Locate parent block in blockchain
        if (not self.blockchain.contains_block(block.blockheader.hash_prev)):
            #Add to orphan blockpool
            self.orphanblocks.add_block(sender, hash, block)
            return ([self.orphanblocks.get_missing_root()], [])
        
        
        #Checks-2 (done after finding the parent block)
        #Prepare verify block
        prevblockiter = self.blockchain.getblockiterator(block.blockheader.hash_prev)
        prevblockheader = prevblockiter.get_blockheader()
        height = prevblockiter.height() + 1
        #Check proof of work
        if (prevblockiter.get_next_work_required() != block.blockheader.bits):
            self.log.info("Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required()))
            incorrect_blocks.append((sender, block, "Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required())))
            return (missing_blocks, incorrect_blocks)
        #Check time stamp
        if (block.blockheader.time <= prevblockiter.get_median_time_past()):
            incorrect_blocks.append((sender, block, "block's timestamp is smaller than the median of past %d block: %d <= %d" % (MEDIAN_TIME_SPAN, prevblockiter.get_blockheader().time , prevblockiter.get_median_time_past())))
            return (missing_blocks, incorrect_blocks)
        #Check that all transactions are finalized (can this be done somewhere else?)
        for tx in block.transactions:
            #for txin in tx.in_list:
            #    self.log.info("txin: sequence : %d" % (txin.sequence))
            if not tx.isfinal(height, block.blockheader.time):
                incorrect_blocks.append((sender, block, "transaction is not final: %s" % str(hash_tx(tx))))
                return (missing_blocks, incorrect_blocks)
        #Verify checkpoints
        if not verify_checkpoints(self.runmode, height, hash):
            incorrect_blocks.append((sender, block, "blockchain checkpoint error: height:%d value:%s != %s" % (height, hash, str(get_checkpoint(self.runmode, height)))))
            return (missing_blocks, incorrect_blocks)
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

