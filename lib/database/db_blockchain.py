# -*- coding:utf-8 -*-
"""
Created on 25 Jul 2011

@author: kris
"""
from bsddb.db import *
import bsddb
import os
from coinpy.model.blockchain.blockchain import BlockChain
from coinpy.lib.database.block_storage import BlockStorage
from coinpy.lib.database.db_blockiterator import DbBlockIterator
from coinpy.lib.database.db_txiterator import DbTxIterator
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.database.objects.blockindex import DbBlockIndex
from coinpy.model.protocol.runmode import MAIN
from coinpy.lib.database.indexdb import IndexDB
from coinpy.model.blockchain.hash import hashblock
from coinpy.model.genesis import GENESIS
from coinpy.lib.database.branch import Branch
from coinpy.lib.database.blockref import BlockRef
from coinpy.lib.hash.hash_block import hash_block

class DBBlockChain(BlockChain):
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
        self.indexdb.create(hashblock(genesis_block), genesis_index)
    
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
    
    def get_transaction_iterator(self, hash):
        return DbTxIterator(self.indexdb, self.blockstore, hash)
    
    def get_block_iterator(self, hash):
        return DbBlockIterator.from_hash(self.indexdb, self.blockstore, hash)
    """
    def getbranch(self, lasthash, firsthash=None):
        if (not self.indexdb.contains_block(lasthash)):
            return (None)
        return Branch(self.indexdb, self.blockstore, lasthash, firsthash)
    
    def getblockref(self, hash):
        if (not self.indexdb.contains_block(hash)):
            return (None)
        return BlockRef(self.indexdb, self.blockstore, hash)
       

    def appendblock(self, blockhash, block):
        #Save it
        file, blockpos = self.blockstore.saveblock(block)
        idx = DbBlockIndex(self.version, uint256(0), file, blockpos, 0, block.blockheader) #height is filled later
        self.indexdb.set_blockindex(blockhash, idx)
        #Add to branch
        brprev = self.getbranch(block.blockheader.hash_prev)
        if not brprev.is_mainchain():
            mainchain_parent = brprev.mainchain_parent()
            altchain = Branch(mainchain_parent, brprev)
            mainchain = Branch(mainchain_parent, self.indexdb.hashbestchain())
            if (altchain.work() + block.blockheader.work() > mainchain.work()):
                self.update_bestbranch(mainchain, altchain)     
        brprev.append(blockhash, idx)
        if self.indexdb.get_blockindex(blockhash).height % 20 == 0:
            self.log.info("Appended block : %d" % self.indexdb.get_blockindex(blockhash).height)
            
            
    def update_bestbranch(self, oldbest, newbest):
        oldbest.set_mainchain(False)
        newbest.set_mainchain(True)
        
        
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
    #0rint db.load_txindex(uint256.from_hexstr("00004b78031f6f406c23cb7d1d0990d56f39107febe8c982a5f75a87254143ea"))

    

