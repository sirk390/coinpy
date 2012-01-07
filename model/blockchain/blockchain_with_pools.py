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
from coinpy.model.constants.bitcoin import TARGET_INTERVAL

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
        
    def verified_add_tx(self, item):
        self.log.info("Adding tx %s" % str(item))
    
    """
        Adds a block to the BlockchainWithPools
            returns: tuple(missing_blocks, errorneous_blocks)
    """
    def add_block(self, sender, hash, block):
        #self.log.info("Adding block %s" % str(block))
        #(hash != self.blockchain.genesishash) and 
            
        if (not self.blockchain.contains_block(block.blockheader.hash_prev)):
            #Add to orphan blockpool
            self.orphanblocks.add_block(sender, hash, block)
            return ([self.orphanblocks.get_missing_root()], [])
        #process / verify block
        prevblockiter = self.blockchain.getblockiterator(block.blockheader.hash_prev)
        #Check proof of work
        if (prevblockiter.get_next_work_required() != block.blockheader.bits):
            self.log.info("Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required()))
            #return ([], [(sender, block, "Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required()))])
        
        #check proof of work
        #if ((prevblock.height  + 1) % TARGET_INTERVAL):
            #same difficulty
        #    nbits = prevblock.blockheader.bits
        #else:
            #recompute difficulty
        #    pass
        #check timestamp
        
        
        
        
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

