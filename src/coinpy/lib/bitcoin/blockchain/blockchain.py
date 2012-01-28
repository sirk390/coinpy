# -*- coding:utf-8 -*-
"""
Created on 24 Jan 2012

@author: kris
"""
from coinpy.lib.bitcoin.blockchain.branch_reorganize import BranchReorganize
from coinpy.lib.bitcoin.blockchain.blockchain_logic import BlockchainLogic
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.lib.bitcoin.blockchain.buffered_tx import BufferedTx
from coinpy.model.constants.bitcoin import COINBASE_MATURITY
from coinpy.model.blockchain.branch import Branch

class Blockchain():
    def __init__(self, database):
        self.database = database
        self.runmode = database.runmode

    def append_block(self, blockhash, block):
        self.database.start_updates()
        brprev = self.get_branch(block.blockheader.hash_prev)
        if not brprev.is_mainchain():
            mainchain_parent = brprev.mainchain_parent()
            altchain = self.get_branch(mainchain_parent, brprev)
            mainchain = self.get_branch(mainchain_parent, self.indexdb.hashbestchain())
            if (altchain.work() + block.blockheader.work() > mainchain.work()):
                self.database.set_mainchain(altchain)
                for block in mainchain:
                    self._disconnect_block(block)
                for block in altchain:
                    self._connect_block(block)
        self.database.add_block(blockhash, block)
        self._connect_block(block)
        self.database.commit_updates()
    
    def get_branch(self, lasthash, firsthash=None):
        if (not self.database.contains_block(lasthash)):
            return (None)
        return Branch(self.log, self.database, lasthash, firsthash)
    
    def getheight(self):
        besthash = self.indexdb.get_hashbestchain() 
        return self.indexdb.get_blockindex(besthash).height
    
    def get_block_locator(self):
        block_locator = []
        current = self.indexdb.get_hashbestchain() 
        stepsize = 1
        while (current != uint256(0)):
            block_locator.append(current)
            
            for i in range(stepsize):
                if (current == uint256(0)):
                    break
                current = self.indexdb.get_blockindex(current).blockheader.hash_prev
            stepsize*= 2
            #tmp speedup hack
            if stepsize == 256:
                break
                
        block_locator.append(self.genesishash)
        return (block_locator)
    
    def _disconnect_block(self, block):
        for tx in block.transactions:
            for txin in tx.in_list:
                tx = self.database.get_transaction_handle(txin.previous_output.hash)
                tx.mark_spent(txin.prevout.n, False)

    def _connect_block(self, block, blockheight):
        for tx in block.transactions:
            txhash = hash_tx(tx)
            for index, txin in enumerate(tx.in_list):
                #fetch inputs
                itf_txprev = self.database.get_transaction_handle(txin.previous_output.hash)
                txprev = itf_txprev.get_transaction()
                #check matured coinbase.
                if (txprev.iscoinbase()):
                    blockprev = txprev.get_block()
                    if (blockheight - blockprev.height < COINBASE_MATURITY):
                        raise Exception("#trying to spend unmatured coins.")
                #verify scripts
                if not self.vm.validate(tx, index, txprev.out_list[txin.previous_output.index].script, tx.in_list[index].script):
                    raise Exception("input scritp/signature validation failed")
                #check double-spend
                if (itf_txprev.is_output_spent(txin.prevout.n)):
                    raise Exception( "output allready spent")
                #mark spent
                itf_txprev.mark_spent(txin.prevout.n, True, txhash)

  