# -*- coding:utf-8 -*-
"""
Created on 10 Jan 2012

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_block import block_encoder
from coinpy.model.constants.bitcoin import MAX_BLOCK_SIZE, PROOF_OF_WORK_LIMIT,\
    MEDIAN_TIME_SPAN
from coinpy.lib.bitcoin.validatation_result import ValidationResult,\
    STATUS_ERROR
from coinpy.lib.bitcoin.merkle_tree import compute_merkle_root
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.model.blockchain.checkpoints import verify_checkpoints,\
    get_checkpoint

class BlockVerifier():
    def __init__(self, runmode):
        self.runmode = runmode
        self.block_serializer = block_encoder()
    
    """
        basic_check: run tests that don't require context or the block parent.
    """
    def basic_checks(self, hash, block):
        result = self._check_tests([self.check_size_limit,
                                    self.check_proof_of_work,
                                    self.check_coinbase,
                                    self.check_merkle_root], 
                                    hash, block)
        return result
    
    def check_size_limit(self, hash, block):
        #FIXME: don't serialize the block here (add get_serialize_size() in serialize objects
        #or cache previoulsy serialized block)
        if (len(self.block_serializer.encode(block)) > MAX_BLOCK_SIZE):
            return (ValidationResult(STATUS_ERROR, "block size limit exceeded"))
    
    def check_proof_of_work(self, hash, block):
        target = block.blockheader.target()
        if (target <= uint256(0) or target > PROOF_OF_WORK_LIMIT[self.runmode]):
            return ValidationResult(STATUS_ERROR, "proof of work: value out of range : %x" % (block.blockheader.bits))
        if (hash > target):
            return ValidationResult(STATUS_ERROR, "proof of work: hash doesn't match target hash:%s, target:%s" % (hash, target))
    
    # not out of context: (check elsewhere) 
    # def check_timestamp(self, hash, block):
    #     block.blockheader.time > time.time
    


    def check_coinbase(self, hash, block):
        if not len(block.transactions):
            return ValidationResult(STATUS_ERROR, "Block has no transactions" )
        if not block.transactions[0].iscoinbase():
            return ValidationResult(STATUS_ERROR, "block's first transactions is not coinbase" )
        for tx in block.transactions[1:]:
            if tx.iscoinbase():
                return ValidationResult(STATUS_ERROR, "more than one coinbase" )
    
    def check_transactions(self, hash, block):
        pass

    def check_merkle_root(self, hash, block):
        merkle = compute_merkle_root(block)
        if merkle != block.blockheader.hash_merkle:
            return ValidationResult(STATUS_ERROR, "merkel root incorrect: %s != %s" % (str(merkle), str(block.blockheader.hash_merkle)) )
    
    """
        verify_block: verify block after finding the parent block.
    """
    def verify_block(self, hash, block, blockchain):
        prevblockiter = blockchain.getblockiterator(block.blockheader.hash_prev)
        prevblockheader = prevblockiter.get_blockheader()
        height = prevblockiter.height() + 1
        
        result = self._check_tests([self.check_target,
                                    self.check_timestamp,
                                    self.check_tx_finalized,
                                    self.check_checkpoints],
                                    prevblockiter, block)
        return result        
        
    def check_target(self, prevblockiter, block):
        #Check proof of work target
        if (prevblockiter.get_next_work_required() != block.blockheader.bits):
            return ValidationResult(STATUS_ERROR, "Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required()) )

            #self.log.info("Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required()))
            #incorrect_blocks.append((sender, block, "Incorrect difficulty target: %08x != %08x" % (block.blockheader.bits, prevblockiter.get_next_work_required())))
        
    def check_timestamp(self, prevblockiter, block):
        if (block.blockheader.time <= prevblockiter.get_median_time_past()):
            return ValidationResult(STATUS_ERROR, "block's timestamp is smaller than the median of past %d block: %d <= %d" % (MEDIAN_TIME_SPAN, prevblockiter.get_blockheader().time , prevblockiter.get_median_time_past()))

    def check_tx_finalized(self, prevblockiter, block):
        height = prevblockiter.height()+1
        #Check that all transactions are finalized (can this be done somewhere else?)
        for tx in block.transactions:
            if not tx.isfinal(height, block.blockheader.time):
                return ValidationResult(STATUS_ERROR, "transaction is not final: %s" % str(hash_tx(tx)))
    
    def check_checkpoints(self, prevblockiter, block):
        height = prevblockiter.height()+1
        if not verify_checkpoints(self.runmode, height, hash):
            return ValidationResult(STATUS_ERROR, "blockchain checkpoint error: height:%d value:%s != %s" % (height, hash, str(get_checkpoint(self.runmode, height))))
        
    # test helper aggregate function
    def _check_tests(self, methods, *args):
        for m in methods:
            result = m(*args)
            if result and result.status == STATUS_ERROR:
                return (result)
        return None
                
        