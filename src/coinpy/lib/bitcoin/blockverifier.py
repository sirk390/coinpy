# -*- coding:utf-8 -*-
"""
Created on 10 Jan 2012

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_block import block_encoder
from coinpy.model.constants.bitcoin import MAX_BLOCK_SIZE, PROOF_OF_WORK_LIMIT
from coinpy.lib.bitcoin.validatation_result import ValidationResult,\
    STATUS_ERROR
from coinpy.lib.bitcoin.merkle_tree import compute_merkle_root
from coinpy.model.protocol.structures.uint256 import uint256

class BlockVerifier():
    def __init__(self, runmode):
        self.runmode = runmode
        self.block_serializer = block_encoder()
    
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
    
    # test helper aggregate function
    def _check_tests(self, hash, block, methods, continue_on_error=False):
        results = []
        
        for m in methods:
            result = m(hash, block)
            if result and result.status == STATUS_ERROR:
                results.append(result)
                if not continue_on_error:
                    return (results)
        return results
                
    """
        basic_check: run tests that don't require context or the block parent.
    """
    def basic_check(self, hash, block):
        results = self._check_tests(hash, block, 
                                   [self.check_size_limit,
                                    self.check_proof_of_work,
                                    self.check_coinbase,
                                    self.check_merkle_root])
        if results:
            return results[0]

        
        