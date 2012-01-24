# -*- coding:utf-8 -*-
"""
Created on 20 Jan 2012

@author: kris
"""
from coinpy.lib.bitcoin.blockchain.buffered_tx import BufferedTx
from coinpy.lib.bitcoin.hash_tx import hash_tx

class BlockchainUpdater():
    def __init__(self, database, blockcgain_logic):
        self.database = database
        self.blockcgain_logic = blockcgain_logic

        self.reorganize = None
        self.appended_block = None
        
        self.added_transactions = set()
        self.removed_transactions = set()
        self.transaction = {}
               
    def reorganise_mainbranch(self, mainbranch_reorganize):
        for blockinter in mainbranch_reorganize.oldmainbranch:
            block = blockinter.get_block()
            #Delete transactions
            for tx in block.transactions:
                self.delete_transaction(tx)
            #Mark input transactions unspent
            self.blockcgain_logic.on_disconnect_block(self, block)
            
        for blockinter in mainbranch_reorganize.newmainbranch:
            block = blockinter.get_block()
            #Verify and mark input transactions spent
            self.blockcgain_logic.on_connect_block(self, block, blockinter.height())
            #Add the transactions
            for tx in block.transactions:
                self.add_transaction(tx)

        self.reorganize = mainbranch_reorganize
        
    def mainchain_appendblock(self, hash, block):
        if (self.reorganize):
            height = self.reorganize.newmainbranch.get_height()
        else:
            height = self.database.get_branch(block.blockheader.hash_prev).get_height()
        self.blockcgain_logic.on_connect_block(self, block, height)
        self.appended_block = (hash, block)
        
    def delete_transaction(self, tx):
        txhash = hash_tx(tx)
        if txhash in self.added_transactions:
            del self.added_transactions[txhash]
        self.removed_transactions.add(txhash)
        
    def add_transaction(self, tx, block):
        txhash = hash_tx(tx)
        if txhash in self.removed_transactions:
            del self.removed_transactions[txhash]
        self.added_transactions.add(txhash)
        tx = BufferedTx(txhash, tx, block, [(False, None) for _ in range(tx.out_list)])
        self.transaction[txhash] = tx
        
    def get_transaction(self, transaction_hash):
        if transaction_hash in self.removed_transactions:
            raise Exception("transactions not found")
        if transaction_hash in self.transaction:
            return self.transaction[self.transaction_hash]
        tx_iter = self.blockchain_base.get_transaction(transaction_hash)
        tx = tx_iter.get_transaction()
        tx = BufferedTx(tx_iter.hash, tx, tx_iter.get_block(), tx_iter.is_output_spent(n) for n in range(tx_iter.output_count()))
        self.transaction[transaction_hash] = tx
        return (tx)

    def commit(self):
        if self.reorganize:
            self.reorganize.newmainbranch.set_mainchain(False)
            self.reorganize.oldmainbranch.set_mainchain(True)
        if self.appended_block:
            blockhash, block = self.appended_block 
            #Save and append block
            blk = self.database.saveblock(blockhash, block)
            brprev = self.database.get_branch(block.blockheader.hash_prev)
            brprev.append(blk)
        for tx in self.transaction:
            #update modified transactions
            if tx.modified:
                for o, (is_spent, in_tx_hash) in tx.outputs_spent.iteritems():
                    dbtx = self.blockchain_base.get_transaction(tx.hash)
                    dbtx.mark_spent(o, is_spent, in_tx_hash)
            
    