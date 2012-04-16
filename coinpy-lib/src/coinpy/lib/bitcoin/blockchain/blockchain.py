# -*- coding:utf-8 -*-
"""
Created on 10 Feb 2012

@author: kris
"""
from coinpy.model.constants.bitcoin import COINBASE_MATURITY, TARGET_INTERVAL,\
    TARGET_TIMESPAN, PROOF_OF_WORK_LIMIT, MEDIAN_TIME_SPAN, TARGET_SPACING
from coinpy.lib.bitcoin.hash_tx import hash_tx
import traceback
from coinpy.lib.vm.vm import TxValidationVM
from coinpy.lib.bitcoin.blockchain.branch import Branch
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.lib.bitcoin.difficulty import compact_difficulty
from coinpy.tools.stat import median
from coinpy.lib.bitcoin.blockchain.block_iterator import BlockIterator
from coinpy.model.protocol.structures.blocklocator import BlockLocator
from coinpy.tools.reactor.asynch import asynch_method
from coinpy.tools.observer import Observable
import sys
from coinpy.model.protocol.runmode import TESTNET

class Blockchain(Observable):
    EVT_APPENDED_BLOCK = Observable.createevent()
    EVT_CONNECTED_BLOCK = Observable.createevent()
    EVT_DISCONNECTED_BLOCK = Observable.createevent()
    EVT_SPENT_OUTPUT = Observable.createevent()
    EVT_UNSPENT_OUTPUT = Observable.createevent()
    EVT_REORGANIZE = Observable.createevent()
    EVT_NEW_HIGHEST_BLOCK = Observable.createevent()
    
    def __init__(self, reactor, log, database):
        super(Blockchain, self).__init__(reactor)
        self.log = log
        self.database = database
        self.vm = TxValidationVM()
        
        #set of unit256(): Not currency persisted as not supported by blkindex.dat
        self.alternate_branches = set()
        
    def contains_transaction(self, transaction_hash):
        return self.database.contains_transaction(transaction_hash)
        
    def get_transaction_handle(self, transaction_hash):
        return self.database.get_transaction_handle(transaction_hash)
    
    def get_branch(self, lasthash, firsthash=None):
        return Branch(self.log, self.database, lasthash, firsthash)
     
    @asynch_method      
    def appendblock(self, blockhash, block):
        self.database.begin_updates()
        try:
            prev = self.database.get_block_handle(block.blockheader.hash_prev)
            self.log.debug("current height: %s, mainchain: %s" % (str(self.get_height()), str(self.database.get_mainchain())))
            self.log.debug("prev height: %s" % str(prev.get_height()))
            append_altbranch = (prev.hash != self.database.get_mainchain())
            reorganize = False
            if append_altbranch:
                self.log.debug("Appending to altbranch")
                if prev.hash in self.alternate_branches:
                    self.alternate_branches.remove(prev.hash)
                mainchain_parent = self.get_mainchain_parent(prev.hash)
                altchain = self.get_branch(prev.hash, mainchain_parent.hash)
                mainchain = self.get_branch(self.database.get_mainchain(), mainchain_parent.hash)
                if (altchain.work() + block.blockheader.work() > mainchain.work()):
                    self.log.info("Reorganize")
                    
                    reorganize = True
                    for blk in mainchain:
                        yield self._disconnect_block(blk)
                    #set_mainchain is required after disconnecting (as disconnect still requires transaction from old mainchain) 
                    #and before connecting (as _connect_block requires transactions from new alternate chain)
                    self.database.set_mainchain(prev.hash) 
                    for blk in altchain.foreward_iterblocks():
                        yield self._connect_block(blk)
            block_handle = self.database.append_block(blockhash, block)
            if not append_altbranch or reorganize:
                yield self._connect_block(block_handle)
            else:
                self.alternate_branches.add(blockhash)
        except Exception as err:
            self.log.error(traceback.format_exc())
            self.database.cancel_updates()
            raise
        self.database.commit_updates()
        # fire events after commit
        if (reorganize):
            self.fire(self.EVT_REORGANIZE)
        if not append_altbranch:
            self.fire(self.EVT_APPENDED_BLOCK, block=block, blockhash=blockhash)
            self._fire_connect_block_events(block, blockhash)
        if not append_altbranch or reorganize:
            self.fire(self.EVT_NEW_HIGHEST_BLOCK, block=block, blockhash=blockhash, height=block_handle.get_height())
        yield block_handle
        
    def _fire_connect_block_events(self, block, blockhash):
        self.fire(self.EVT_CONNECTED_BLOCK, block=block, blockhash=blockhash)
        for tx in block.transactions:
            if not tx.iscoinbase():
                for index in range(len(tx.in_list)):
                    #txhash = hash_tx(tx)
                    handle = self.database.get_transaction_handle(tx.in_list[index].previous_output.hash)
                    self.fire(self.EVT_SPENT_OUTPUT, txhash=handle.hash, index=index)

    def get_next_in_mainchain(self, blockhash):
        return self.database.get_next_in_mainchain(blockhash)
    
    def contains_block(self, blockhash):
        return self.database.contains_block(blockhash)

    def get_block_handle(self, blockhash):
        return self.database.get_block_handle(blockhash)
    
    def get_block(self, blockhash):
        return self.database.get_block_handle(blockhash).get_block()

    def get_height(self):
        handlebest = self.database.get_block_handle(self.database.get_mainchain())
        return handlebest.get_height()
     
    def _disconnect_block(self, block_handle):
        for tx in block_handle.get_block().transactions:
            if not tx.iscoinbase():
                for txin in tx.in_list:
                    tx = self.database.get_transaction_handle(txin.previous_output.hash)
                    tx.mark_spent(txin.previous_output.index, False)

    @asynch_method      
    def _connect_block(self, block_handle):
        #self.log.info("Connecting block : %d (%d transactions)" % (block_handle.get_height(), len(block_handle.get_block().transactions)))    
        for tx in block_handle.get_block().transactions:
            if not tx.iscoinbase():
                txhash = hash_tx(tx)
                for index in range(len(tx.in_list)):
                    yield self._connect_txin(tx, txhash, index, block_handle)
                    
    @asynch_method      
    def _connect_txin(self, tx, txhash, index, block_handle):
        txin = tx.in_list[index]
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
            raise Exception("input scritp/signature validation failed")
        #check double-spend
        if (txprev_handle.is_output_spent(txin.previous_output.index)):
            spending_tx = txprev_handle.get_spending_transaction(txin.previous_output.index)
            raise Exception( "Output allready spent in block:%s,tx:%s. Output:%s:%d of block:%s allready spent in tx:%s of block:%s" %(str(block_handle.hash), str(txhash), str(txin.previous_output.hash), txin.previous_output.index, str(txprev_handle.get_block().hash), spending_tx.hash, str(spending_tx.get_block().hash)))
        #mark spent
        txprev_handle.mark_spent(txin.previous_output.index, True, txhash)
        #self.log.info("txin %s:%d connected" % (str(txin.previous_output.hash), txin.previous_output.index))    
        yield None
        
    def get_mainchain_parent(self, blockhash):
        handle = self.database.get_block_handle(blockhash)
        while not handle.is_mainchain() and handle.hasprev():
            handle = self.database.get_block_handle(handle.get_blockheader().hash_prev)
        return handle
    
    def get_block_locator(self):
        block_locator = list(self.alternate_branches) # TODO: reset alternate_branches during rebranches?
        it = BlockIterator(self.database, self.database.get_mainchain())
        stepsize = 1
        while (it.hash != self.database.genesishash):
            block_locator.append(it.hash)
            i = 0
            while it.hasprev() and i < stepsize:
                it.prev()
                i += 1
            stepsize*= 2
            #tmp speedup hack
            #if stepsize >= 256:
            #    break           
        block_locator.append(self.database.genesishash)
        return BlockLocator(1, block_locator)
    
    # Get testnet work required after 15 Feb 2012
    def get_testnet_work_required_15feb1012(self, blkprev, block):
        #If there is not block during 2*TARGET_SPACING, reset difficulty to min-difficilty
        if (block.blockheader.time - blkprev.get_blockheader().time > TARGET_SPACING * 2 or 
            block.blockheader.time < blkprev.get_blockheader().time):
            new_target = PROOF_OF_WORK_LIMIT[self.database.runmode]
        else:
            #otherwise, keep the last non-special difficulty
            while blkprev and blkprev.get_height() % TARGET_INTERVAL != 0 and blkprev.get_blockheader().bits == compact_difficulty(PROOF_OF_WORK_LIMIT[self.database.runmode]):
                blkprev = self.database.get_block_handle(blkprev.get_blockheader().hash_prev)
            new_target = blkprev.get_blockheader().target()
        return compact_difficulty(new_target)
    
    #GetNextWorkRequired: main.cpp:819
    def get_next_work_required(self, blkprevhash, block):
        blkprev = self.database.get_block_handle(blkprevhash)
        # Difficulty changes only once every TARGET_INTERVAL blocks (except for testnet)
        if ((blkprev.get_height() + 1) % TARGET_INTERVAL):
            # Special rules for testnet after 15 Feb 2012
            if self.database.runmode == TESTNET: 
                if (block.blockheader.time > 1329264000):
                    return self.get_testnet_work_required_15feb1012(blkprev, block)
            # Difficulty unchanged
            return (blkprev.get_blockheader().bits)
        # Locate the block 2 weeks ago
        blk2weekago = blkprev
        for i in range(TARGET_INTERVAL-1):
            blk2weekago = self.database.get_block_handle(blk2weekago.get_blockheader().hash_prev)
        header_block2weekago = blk2weekago.get_blockheader()
        header_blocknow = blkprev.get_blockheader()
        
        actual_timespan = header_blocknow.time - header_block2weekago.time
        # Limit adjustment step
        if actual_timespan < TARGET_TIMESPAN/4:
            actual_timespan = TARGET_TIMESPAN/4;
        if actual_timespan > TARGET_TIMESPAN*4:
            actual_timespan = TARGET_TIMESPAN*4;
    
        # Retarget
        new_target = Uint256.from_bignum(header_blocknow.target().get_bignum() * actual_timespan / TARGET_TIMESPAN)
        if new_target > PROOF_OF_WORK_LIMIT[self.database.runmode]:
            new_target = PROOF_OF_WORK_LIMIT[self.database.runmode]
        new_bits = compact_difficulty(new_target)
        self.log.info("Retarget: targetTimespan:%d actualTimespan:%d, %08x -> %08x " % (TARGET_TIMESPAN, actual_timespan, header_blocknow.bits, new_bits))
        return (new_bits)
    
    #ref main.h:1109
    def get_median_time_past(self, hashprev):
        block_times = []
        i = 0
        while hashprev != Uint256.zero() and i < MEDIAN_TIME_SPAN:
            blk = self.database.get_block_handle(hashprev)
            blkheader = blk.get_blockheader()
            block_times.append(blkheader.time)
            hashprev = blkheader.hash_prev
            i += 1
        return median(block_times)
