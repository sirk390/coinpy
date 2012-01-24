# -*- coding:utf-8 -*-
"""
Created on 25 Jul 2011

@author: kris
"""
from bsddb.db import *
import bsddb
import os
from coinpy.lib.database.block_storage import BlockStorage
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.database.objects.blockindex import DbBlockIndex
from coinpy.model.protocol.runmode import MAIN
from coinpy.lib.database.indexdb import IndexDB
from coinpy.model.genesis import GENESIS
from coinpy.lib.database.branch import Branch
from coinpy.lib.bitcoin.hash_block import hash_block
from coinpy.lib.database.db_txinterface import DBTxInterface
from coinpy.lib.database.db_blockinterface import DBBlockInterface
from coinpy.model.blockchain.blockchain_database import BlockChainDatabase

class BSDDbBlockChainDatabase(BlockChainDatabase):
    def __init__(self, log, runmode, directory="."):
        self.log = log
        self.runmode = runmode
        self.indexdb = IndexDB(runmode, directory)
        self.blockstore = BlockStorage(runmode, directory)
        self.version = 32200

    def open(self):
        self.indexdb.open()
        
    def exists(self):
        return (self.indexdb.exists())

    def create(self, genesis_block):
        file, blockpos = self.blockstore.saveblock(genesis_block)
        genesis_index = DbBlockIndex(self.version, uint256(0), file, blockpos, 0, genesis_block.blockheader)
        self.indexdb.create(hash_block(genesis_block), genesis_index)
    
    def open_or_create(self, genesisblock):
        self.genesisblock = genesisblock
        self.genesishash = hash_block(genesisblock)
        if self.exists():
            self.open()
        else:
            self.create(genesisblock)
    
    
    def contains_block(self, hash):
        return self.indexdb.contains_block(hash)
    """
    def contains_transaction(self, hash):
        return self.indexdb.contains_transaction(hash)
    """    
    def get_transaction(self, hash):
        return DBTxInterface(self.log, self.indexdb, self.blockstore, hash)
    

    def get_branch(self, lasthash, firsthash=None):
        if (not self.indexdb.contains_block(lasthash)):
            return (None)
        return Branch(self.log, self.indexdb, self.blockstore, lasthash, firsthash)
    
    def get_block(self, hash):
        if (not self.indexdb.contains_block(hash)):
            return (None)
        return DBBlockInterface(self.log, self.indexdb, self.blockstore, hash)
   
    def saveblock(self, blockhash, block):
        file, blockpos = self.blockstore.saveblock(block)
        prevblockiter = self.get_block(block.blockheader.hash_prev)
        idx = DbBlockIndex(self.version, uint256(0), file, blockpos, prevblockiter.get_height()+1, block.blockheader)
        self.indexdb.set_blockindex(blockhash, idx)
        return DBBlockInterface(self.log, self.indexdb, self.blockstore, hash, idx)
               
    def update_bestbranch(self, oldbest, newbest):
        oldbest.set_altchain()
        newbest.set_mainchain()
        
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

if __name__ == '__main__':
    """db = DBBlockChain(MAIN, directory=".")
    if not db.exists():
        print "Creating database"
        db.create(GENESIS)
    else:
        print "Opening database"
        db.open()
    
        version
        hashBestChain"""
    db = DBBlockChain(MAIN, directory="../../data")
    db.open()
    from coinpy.model.protocol.structures.uint256 import uint256
    print db.indexdb.hashbestchain()
    print db.contains_block(uint256.from_hexstr("00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048"))
    print db.contains_block(uint256.from_hexstr("00000000139a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048"))
    it = db.get_block_iterator(uint256.from_hexstr("000000000000029b4b03122dc75e22952e574ded1ba7caef1fd81c1d11f08e73"))
    print it.get_block()
    print db.indexdb.hashbestchain()
    print db.get_block_iterator(db.indexdb.hashbestchain())
    
    #
    print db.contains_transaction(uint256.from_hexstr("f8780c27a0af1eb62968a5ab20417f706706f3fa7316775ae0f59850bb757c72"))
    print db.get_transaction_iterator(uint256.from_hexstr("f8780c27a0af1eb62968a5ab20417f706706f3fa7316775ae0f59850bb757c72"))
    it = db.get_transaction_iterator(uint256.from_hexstr("f8780c27a0af1eb62968a5ab20417f706706f3fa7316775ae0f59850bb757c72"))
    
    print db.get_block_iterator(db.indexdb.hashbestchain()).get_block()
    #db.addblock("hello")
    #db.load_owner_transactions(owner1)
    #print db.load_txindex(uint256.from_hexstr("00004b78031f6f406c23cb7d1d0990d56f39107febe8c982a5f75a87254143ea"))

    

