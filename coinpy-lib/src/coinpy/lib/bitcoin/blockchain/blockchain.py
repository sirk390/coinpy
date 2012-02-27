# -*- coding:utf-8 -*-
"""
Created on 10 Feb 2012

@author: kris
"""
from coinpy.model.constants.bitcoin import COINBASE_MATURITY, TARGET_INTERVAL,\
    TARGET_TIMESPAN, PROOF_OF_WORK_LIMIT, MEDIAN_TIME_SPAN
from coinpy.lib.bitcoin.hash_tx import hash_tx
import traceback
from coinpy.lib.vm.vm import TxValidationVM
from coinpy.lib.bitcoin.blockchain.branch import Branch
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.bitcoin.difficulty import compact_difficulty
from coinpy.tools.stat import median
from coinpy.lib.bitcoin.blockchain.block_iterator import BlockIterator
from coinpy.model.protocol.structures.blocklocator import BlockLocator
from coinpy.tools.reactor.asynch import asynch_method
from coinpy.tools.observer import Observable

class Blockchain(Observable):
    EVT_APPENDED_BLOCK = Observable.createevent()
    EVT_CONNECTED_BLOCK = Observable.createevent()
    EVT_DISCONNECTED_BLOCK = Observable.createevent()
    EVT_SPENT_OUTPUT = Observable.createevent()
    EVT_UNSPENT_OUTPUT = Observable.createevent()
    EVT_REORGANIZE = Observable.createevent()
    EVT_NEW_HIGHEST_BLOCK = Observable.createevent()
    
    def __init__(self, log, database):
        super(Blockchain, self).__init__()
        self.log = log
        self.database = database
        self.vm = TxValidationVM()
    
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
            append_altbranch, reorganize = not prev.is_mainchain(), False
            if append_altbranch:
                mainchain_parent = self.get_mainchain_parent(prev.hash)
                altchain = self.get_branch(prev.hash, mainchain_parent.hash)
                mainchain = self.get_branch(self.database.get_mainchain(), mainchain_parent.hash)
                if (altchain.work() + block.blockheader.work() > mainchain.work()):
                    reorganize = True
                    self.database.set_mainchain(prev.hash)
                    for block in mainchain:
                        self._disconnect_block(block)
                    for block in altchain:
                        yield self._connect_block(block)
                    
            block_handle = self.database.append_block(blockhash, block)
            yield self._connect_block(block_handle)
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
        
    def contains_block(self, blockhash):
        return self.database.contains_block(blockhash)

    def get_height(self):
        handlebest = self.database.get_block_handle(self.database.get_mainchain())
        return handlebest.get_height()
     
    def _disconnect_block(self, block_handle):
        for tx in block_handle.get_block().transactions:
            for txin in tx.in_list:
                tx = self.database.get_transaction_handle(txin.previous_output.hash)
                tx.mark_spent(txin.prevout.n, False)

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
            raise Exception( "output allready spent")
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
        return BlockLocator(1, block_locator)
    
    def get_next_work_required(self):
        if ((self.get_height() + 1) % TARGET_INTERVAL):
            # Difficulty unchanged
            return (self.get_blockheader().bits)
        
        # Locate the block 2 weeks ago
        it2weekago = BlockIterator(self.database, self.hash)
        for i in range(TARGET_INTERVAL-1):
            it2weekago.prev()
        header_block2weekago = it2weekago.get_blockheader()
        header_blocknow = self.get_blockheader()
        
        actual_timespan = header_blocknow.time - header_block2weekago.time
        # Limit adjustment step
        if actual_timespan < TARGET_TIMESPAN/4:
            actual_timespan = TARGET_TIMESPAN/4;
        if actual_timespan > TARGET_TIMESPAN*4:
            actual_timespan = TARGET_TIMESPAN*4;
    
        # Retarget
        new_target = uint256.from_bignum(header_blocknow.target().get_bignum() * actual_timespan / TARGET_TIMESPAN)
        if new_target > PROOF_OF_WORK_LIMIT[self.indexdb.runmode]:
            new_target = PROOF_OF_WORK_LIMIT[self.indexdb.runmode]
        new_bits = compact_difficulty(new_target)
        self.log.info("Retarget: targetTimespan:%d actualTimespan:%d, %08x -> %08x " % (TARGET_TIMESPAN, actual_timespan, header_blocknow.bits, new_bits))
        return (new_bits)
    
    #ref main.h:1109
    def get_median_time_past(self):
        block_times = []
        #TODO replace with "branch"
        iter = BlockIterator(self.database, self.hash)
        for dummy in range(MEDIAN_TIME_SPAN):
            block_times.append(iter.get_blockheader().time)
            if (not iter.prev()):
                break;
        return median(block_times)
