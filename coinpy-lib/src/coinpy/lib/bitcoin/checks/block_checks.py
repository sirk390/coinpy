# -*- coding:utf-8 -*-
"""
Created on 10 Jan 2012

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_block import BlockSerializer
from coinpy.model.constants.bitcoin import MAX_BLOCK_SIZE, PROOF_OF_WORK_LIMIT,\
    MEDIAN_TIME_SPAN
from coinpy.lib.bitcoin.merkle_tree import compute_merkle_root
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.model.blockchain.checkpoints import verify_checkpoints,\
    get_checkpoint
from coinpy.lib.bitcoin.checks.tx_checks import TxVerifier
import pickle

class BlockVerifier():
    def __init__(self, runmode):
        self.runmode = runmode
        self.block_serializer = BlockSerializer()
        self.tx_verifier = TxVerifier(self.runmode)
        
    """
        basic_check: run tests that don't require context or the block parent.
    """
    def basic_checks(self, hash, block):
        self.check_size_limit(hash, block)
        self.check_proof_of_work(hash, block)
        self.check_coinbase(hash, block)
        self.check_transactions(hash, block)
        self.check_merkle_root(hash, block)
                                    

    def check_size_limit(self, hash, block):
        #FIXME: don't serialize the block here (add get_serialize_size() in serialize objects
        #or cache previoulsy serialized block)
        if (not block.rawdata):
            block.rawdata = self.block_serializer.serialize(block)
        if len(block.rawdata) > MAX_BLOCK_SIZE:
            raise Exception("block size limit exceeded")
    
    def check_proof_of_work(self, hash, block):
        target = block.blockheader.target()
        if (target <= uint256.zero() or target > PROOF_OF_WORK_LIMIT[self.runmode]):
            raise Exception("proof of work: value out of range : %x" % (block.blockheader.bits))
        if (hash > target):
            raise Exception("proof of work: hash doesn't match target hash:%s, target:%s" % (hash, target))
    
    # not out of context: (check elsewhere) 
    # def check_timestamp(self, hash, block):
    #     block.blockheader.time > time.time
    


    def check_coinbase(self, hash, block):
        if not len(block.transactions):
            raise Exception("Block has no transactions" )
        if not block.transactions[0].iscoinbase():
            raise Exception("block's first transactions is not coinbase" )
        for tx in block.transactions[1:]:
            if tx.iscoinbase():
                raise Exception("more than one coinbase" )
    
    def check_transactions(self, hash, block):
        for tx in block.transactions:
            err = self.tx_verifier.basic_checks(tx)
            if err:
                return err

    def check_merkle_root(self, hash, block):
        merkle = compute_merkle_root(block)
        if merkle != block.blockheader.hash_merkle:
            with open("block_%s.pkl" % hash, "wb") as f:
                pickle.dump(block, f)
            raise Exception("merkel root incorrect for block %s: %s != %s" % (str(hash), str(merkle), str(block.blockheader.hash_merkle)) )
            
    """
        accept_block: check block after finding the parent block.
    """
    #AcceptBlock: main.cpp:1445
    def accept_block(self, hash, block, blockchain):
        prevblockiter = blockchain.get_block(block.blockheader.hash_prev)
        
        self.check_target(prevblockiter, hash, block)
        self.check_timestamp(prevblockiter, hash, block)
        self.check_tx_finalized(prevblockiter, hash, block)
        self.check_checkpoints(prevblockiter, hash, block)
      
        
    def check_target(self, prevblockiter, hash, block):
        #Check proof of work target
        if (prevblockiter.get_next_work_required() != block.blockheader.bits):
            raise Exception("Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required()) )

            #self.log.info("Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required()))
            #incorrect_blocks.append((sender, block, "Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required())))
        
    def check_timestamp(self, prevblockiter, hash, block):
        if (block.blockheader.time <= prevblockiter.get_median_time_past()):
            raise Exception("block's timestamp is smaller than the median of past %d block: %d <= %d" % (MEDIAN_TIME_SPAN, prevblockiter.get_blockheader().time , prevblockiter.get_median_time_past()))

    def check_tx_finalized(self, prevblockiter, hash, block):
        height = prevblockiter.get_height()+1
        #Check that all transactions are finalized (can this be done somewhere else?)
        for tx in block.transactions:
            if not tx.isfinal(height, block.blockheader.time):
                raise Exception("transaction is not final: %s" % str(hash_tx(tx)))
    
    def check_checkpoints(self, prevblockiter, hash, block):
        height = prevblockiter.get_height()+1
        if not verify_checkpoints(self.runmode, height, hash):
            raise Exception("blockchain checkpoint error: height:%d value:%s != %s" % (height, hash, str(get_checkpoint(self.runmode, height))))
        

        