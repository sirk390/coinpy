# -*- coding:utf-8 -*-
"""
Created on 24 Jan 2012

@author: kris
"""
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.model.constants.bitcoin import COINBASE_MATURITY
from coinpy.lib.bitcoin.blockchain.block_iterator import BlockIterator
import traceback
from coinpy.lib.bitcoin.blockchain.branch import Branch
from coinpy.lib.vm.vm import TxValidationVM

class Blockchain():
    def __init__(self, log, database):
        self.log = log
        self.database = database
        self.runmode = database.runmode
        self.vm = TxValidationVM()
        
    def appendblock(self, blockhash, block):
        self.database.begin_updates()
        try:
            prev = BlockIterator(self.database, block.blockheader.hash_prev)
            if not prev.is_mainchain():
                mainchain_parent = prev.mainchain_parent()
                altchain = self.get_branch(mainchain_parent.hash, prev.hash)
                mainchain = self.get_branch(mainchain_parent.hash, self.database.get_mainchain())
                if (altchain.work() + block.blockheader.work() > mainchain.work()):
                    self.database.set_mainchain(altchain.lasthash)
                    for block in mainchain:
                        self._disconnect_block(block)
                    for block in altchain:
                        self._connect_block(block)
                    
            block_handle = self.database.append_block(blockhash, block)
            self._connect_block(block_handle)
            #self.database.set_mainchain(blockhash) 
        except:
            traceback.print_exc()
            self.database.cancel_updates()
            raise
        self.database.commit_updates()
        return block_handle
        
    def get_branch(self, lasthash, firsthash=None):
        if (not self.database.contains_block(lasthash)):
            return (None)
        return Branch(self.log, self.database, lasthash, firsthash)
    
    def contains_transaction(self, txhash):
        return self.database.contains_transaction(txhash)
    
    def contains_block(self, blockhash):
        return self.database.contains_block(blockhash)
    
    def get_height(self):
        handlebest = self.database.get_block_handle(self.database.get_mainchain())
        return handlebest.get_height()
    
    def get_block_locator(self):
        block_locator = []
        it = BlockIterator(self.database, self.database.get_mainchain())
        stepsize = 1
        while (it.hash != self.database.genesishash):
            block_locator.append(it.hash)
            for i in range(stepsize):
                it.prev()
            stepsize*= 2
            #tmp speedup hack
            if stepsize >= 256:
                break           
        block_locator.append(self.database.genesishash)
        return (block_locator)
    
    def _disconnect_block(self, block_handle):
        for tx in block_handle.get_block().transactions:
            for txin in tx.in_list:
                tx = self.database.get_transaction_handle(txin.previous_output.hash)
                tx.mark_spent(txin.prevout.n, False)

    def _connect_block(self, block_handle):
        for tx in block_handle.get_block().transactions:
            if not tx.iscoinbase():
                txhash = hash_tx(tx)
                for index, txin in enumerate(tx.in_list):
                    #fetch inputs
                    txprev_handle = self.database.get_transaction_handle(txin.previous_output.hash)
                    txprev = txprev_handle.get_transaction()
                    #check matured coinbase.
                    if (txprev.iscoinbase()):
                        blockprev = txprev_handle.get_block()
                        if (block_handle.get_height() - blockprev.get_height() < COINBASE_MATURITY):
                            raise Exception("#trying to spend unmatured coins.")
                    #verify scripts
                    if not self.vm.validate(tx, index, txprev.out_list[txin.previous_output.index].script, tx.in_list[index].script):
                        print tx.in_list[index].script
                        print txprev.out_list[txin.previous_output.index].script
                        raise Exception("input scritp/signature validation failed")
                    #check double-spend
                    if (txprev_handle.is_output_spent(txin.previous_output.index)):
                        raise Exception( "output allready spent")
                    #mark spent
                    txprev_handle.mark_spent(txin.previous_output.index, True, txhash)
                    self.log.info("txin %s:%d connected" % (str(txin.previous_output.hash), txin.previous_output.index))    
  