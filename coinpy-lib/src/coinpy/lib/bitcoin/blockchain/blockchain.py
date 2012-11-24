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
from coinpy.model.protocol.runmode import TESTNET, TESTNET3
from coinpy.lib.bitcoin.blockchain.blockchain_update import Reorganize, Append

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
        
        #set of unit256(): Not currency persisted as not supported by blkindex.dat
        
    def contains_transaction(self, transaction_hash):
        return self.database.contains_transaction(transaction_hash)
        
    def get_transaction_handle(self, transaction_hash):
        return self.database.get_transaction_handle(transaction_hash)
    
    """ return a list of (hash, block) from firsthash(not included) to lasthash """ 
    def get_branch_blocks(self, lasthash, firsthash=None):
        blocks = []
        pos = self.get_block_handle(lasthash)
        while pos.hasprev() and pos.hash != firsthash:
            blocks.append((pos.hash, pos.get_block()))
            pos = self.database.get_block_handle(pos.blockindex.blockheader.hash_prev)
        blocks.reverse()
        return blocks

    """ Return (txout, height, iscoinbase) corresponding to an outpoint """
    def get_outpoint(self, outpoint):
        tx_handle = self.database.get_transaction_handle(outpoint.hash)
        tx = tx_handle.get_transaction()
        if not (0 <= outpoint.index < len(tx.out_list)):
            return  Exception("Outpoint not found")
        return (tx.out_list[outpoint.index], tx_handle.get_block().get_height(), tx.iscoinbase())


    def get_work_after_block(self, blckhash):
        pos = self.database.get_block_handle(self.get_bestblock())
        work = 0
        while pos.hasprev() and pos.hash != blckhash:
            blockheader = pos.get_blockheader()
            work += blockheader.work()
            pos = self.database.get_block_handle(blockheader.hash_prev)
        return work
    
    def apply_modifications(self, updates):
        self.database.begin_updates()
        for upd in updates:
            if type(upd) is Reorganize:
                for blkhash, blk in reversed(upd.old_mainchain):
                    self._mark_blockinputs_spent(blk, False)
                self.database.reorganize(upd) 
                for blkhash, blk in upd.new_mainchain:
                    self._mark_blockinputs_spent(blk, True)
            if type(upd) is Append:
                self.database.append_block(upd.blockhash, upd.block)
        self.database.commit_updates()
    
        for upd in updates:
            if type(upd) is Append:
                self.fire(self.EVT_NEW_HIGHEST_BLOCK,  blkhash=upd.blockhash, height=self.get_height())
            if type(upd) is Reorganize:
                for blkhash, blk in upd.new_mainchain:
                    self.fire(self.EVT_NEW_HIGHEST_BLOCK, blkhash=blkhash, height=self.get_height())
                
    def _mark_blockinputs_spent(self, block, spent=True):
        for tx in block.transactions:
            txhash = hash_tx(tx)
            if not tx.iscoinbase():        
                for txin in tx.in_list:
                    txprev_handle = self.database.get_transaction_handle(txin.previous_output.hash)
                    txprev_handle.mark_spent(txin.previous_output.index, spent, txhash)

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

    def get_bestblock(self):
        return self.database.get_mainchain()
    
    def get_height(self):
        handlebest = self.database.get_block_handle(self.database.get_mainchain())
        return handlebest.get_height()
     
    def get_block_locator(self):
        block_locator = []
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
            #if stepsize >= 128:
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
            if ((self.database.runmode == TESTNET and (block.blockheader.time > 1329264000))  
                or (self.database.runmode == TESTNET3)):
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