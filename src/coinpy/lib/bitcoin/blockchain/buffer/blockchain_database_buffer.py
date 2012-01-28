# -*- coding:utf-8 -*-
"""
Created on 27 Jan 2012

@author: kris
"""
from coinpy.lib.bitcoin.blockchain.buffer.memblockhandle import MemBlockHandle
from coinpy.lib.bitcoin.blockchain.buffer.memtxhandle import MemTxHandle
from coinpy.lib.bitcoin.hash_tx import hash_tx

class BlockchainDatabaseBuffer():
    SET_MAINCHAIN, ADD_BLOCK = OPERATIONS = range(2)
    
    def __init__(self, database):
        self.database = database
        self.start_updates()
    
    def start_updates(self):
        self.buffered_modifications = []
        #mainchain
        self.ismainchain = {}
        self.mainchainhash = None
        #blocks
        self.added_blocks = {}
        #txs
        self.removed_transactions = set()
        self.added_transactions = set()
        self.transactions = {}
        
    def commit_updates(self):
        #reorganize blockchain
        for op, args in self.buffered_modifications:
            if op == self.SET_MAINCHAIN:
                self.database.set_mainchain(*args)
            if op == self.ADD_BLOCK:
                self.database.add_block(*args)
        #update transactions spent status
        for tx in self.transactions:
            if tx.modified:
                for o, (is_spent, in_tx_hash) in tx.outputs_spent.iteritems():
                    dbtx = self.database.get_transaction_handle(tx.hash)
                    dbtx.mark_spent(o, is_spent, in_tx_hash)
        self.start_updates()    
    
    def get_transaction_handle(self, hash):
        if hash in self.removed_transactions:
            raise Exception("transactions not found")
        if hash in self.transactions:
            return self.transactions[self.transaction_hash]
        dbtxhandle = self.database.get_transaction_handle(hash)
        txhandle = MemTxHandle(dbtxhandle)
        self.transactions[hash] = txhandle
        return txhandle

    def get_block_handle(self, hash):
        if hash in self.added_blocks:
            return self.added_blocks[hash]
        return self.database.get_block_handle(hash)
    
    def add_block(self, blockhash, block):
        prev_handle = self.get_block_handle(block.blockheader.hash_prev)
        handle = MemBlockHandle(block, prev_handle.get_height() + 1)
        self.added_blocks[blockhash] = handle
    
    def _add_transactions(self, blockhash):
        block = self.get_block_handle(blockhash).get_block()
        for tx in block.transaction:
            txhash = hash_tx(tx)
            if txhash in self.removed_transactions:
                del self.removed_transactions[txhash]
            self.added_transactions.add(txhash)
            self.transactions[tx] = MemTxHandle(txhash, tx, block, [(False, None) for _ in range(tx.out_list)])
            
    def _remove_transactions(self, blockhash):
        block = self.get_block_handle(blockhash).get_block()
        for tx in block.transaction:
            txhash = hash_tx(tx)
            if txhash in self.added_transactions:
                del self.added_transactions[txhash]
            self.removed_transactions.add(txhash)
            
    def get_mainchain(self):
        return self.mainchainhash or self.database.get_mainchain()
    
    def set_mainchain(self, new_mainchain_hash):
        #append operation for commit
        self.buffered_modifications.append((self.SET_MAINCHAIN , new_mainchain_hash))
        #Set new mainchain
        hash = new_mainchain_hash
        while not self.is_mainchain(hash):
            self.ismainchain[hash] = True
            self._add_transactions(hash)
            hash = self.get_block_handle(hash).get_blockheader().hash_prev
        #Erase previous one
        hashfork = hash
        hash = self.get_mainchain()
        while hash != hashfork:
            self.ismainchain[hash] = False
            self._remove_transactions(hash)
            hash = self.get_block_handle(hash).get_blockheader().hash_prev
        #Set best
        self.mainchainhash = new_mainchain_hash    
        
    def is_mainchain(self, hash):
        if hash in self.ismainchain:
            return self.ismainchain[hash]
        return self.database.ismainchain(hash)
    
