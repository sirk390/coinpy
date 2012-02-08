# -*- coding:utf-8 -*-
"""
Created on 25 Jul 2011

@author: kris
"""

from coinpy.lib.database.block_storage import BlockStorage
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.database.objects.blockindex import DbBlockIndex
from coinpy.model.protocol.runmode import MAIN
from coinpy.lib.database.indexdb import IndexDB
from coinpy.lib.bitcoin.hash_block import hash_block
from coinpy.model.blockchain.blockchain_database import BlockChainDatabase
from coinpy.lib.database.db_blockhandle import DBBlockHandle
from coinpy.lib.database.db_txhandle import DBTxHandle
from coinpy.lib.database.objects.txindex import DbTxIndex
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.lib.database.objects.disktxpos import DiskTxPos
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer

class BSDDbBlockChainDatabase(BlockChainDatabase):
    def __init__(self, log, runmode, directory="."):
        self.log = log
        self.runmode = runmode
        self.indexdb = IndexDB(runmode, directory)
        self.blockstore = BlockStorage(runmode, directory)
        self.version = 32200
        self.genesishash = None
        self.genesisblock = None

    def open(self):
        self.indexdb.open()
        self.genesishash = self.indexdb.get_hashbestchain()
        self.genesisblock = self.get_block_handle(self.genesishash).get_block()    
    
    def exists(self):
        return (self.indexdb.exists())

    def create(self, genesis_block):
        self.genesisblock = genesis_block
        self.genesishash = hash_block(genesis_block)
        file, blockpos = self.blockstore.saveblock(genesis_block)
        genesis_index = DbBlockIndex(self.version, uint256(0), file, blockpos, 0, genesis_block.blockheader)
        self.indexdb.create(hash_block(genesis_block), genesis_index)
    
    def open_or_create(self, genesisblock):
        if self.exists():
            self.open()
        else:
            self.create(genesisblock)
            
    def begin_updates(self):
        self.indexdb.begin_updates()
        
    def commit_updates(self):
        self.indexdb.commit_updates()

    def cancel_updates(self):
        self.indexdb.abort_updates()
         
    """
        Transaction Operations
    """    
    def get_transaction_handle(self, hash):
        return DBTxHandle(self.log, self.indexdb, self.blockstore, hash)
    
    def contains_transaction(self, txhash):
        return self.indexdb.contains_transaction(txhash)
    
    """
        Block Operations
    """    
    def contains_block(self, blockhash):
        return self.indexdb.contains_block(blockhash)
    
    def get_block_handle(self, blockhash):
        return DBBlockHandle(self.log, self.indexdb, self.blockstore, blockhash)

    def append_block(self, blockhash, block):
        file, blockpos = self.blockstore.saveblock(block)
        prevblock = self.get_block_handle(block.blockheader.hash_prev)
        
        idx = DbBlockIndex(self.version, uint256(0), file, blockpos, prevblock.get_height()+1, block.blockheader)
        self.indexdb.set_blockindex(blockhash, idx)
        if prevblock.is_mainchain():
            prevblock.blockindex.hash_next = blockhash
            self.indexdb.set_blockindex(prevblock.hash, prevblock.blockindex)
            self.indexdb.set_hashbestchain(blockhash)
            self._index_transactions(blockhash)
        return DBBlockHandle(self.log, self.indexdb, self.blockstore, blockhash)

    """
        Mainchain Operations
    """    
    def _find_fork(self, altchainhash):
        hash = altchainhash
        while hash != uint256(0):
            handle = self.get_block_handle(hash)
            if handle.is_mainchain():
                return hash
            hash = handle.get_blockheader().hash_prev 
        return handle.hash
    
    # iterate backwards through [hashfirst-hashlast] blocks and set the 
    # hash_next pointer depending on ismainchain
    def _set_branch(self, hashfirst, hashlast, ismainchain=True):
        hash, nexthash = hashlast, uint256(0)
        while (hash != hashfirst):
            if ismainchain:
                blockindex = self.indexdb.get_blockindex(hash)
                blockindex.hash_next = nexthash
                self.indexdb.set_blockindex(hash, blockindex)
                self._index_transactions(hash)
            else:
                blockindex = self.indexdb.get_blockindex(hash)
                blockindex.hash_next = uint256(0)
                self.indexdb.set_blockindex(hash, blockindex)
                self._unindex_transactions(hash)
            nexthash = hash
        
    def set_mainchain(self, new_mainchain_hash):
        hashfork = self._find_fork(new_mainchain_hash)
        #set hash_next to 0 in previous mainchain
        self._set_branch(hashfork, self.indexdb.get_hashbestchain(), False)
        #set hash_next to next in new mainchain
        self._set_branch(hashfork, new_mainchain_hash, True)
        #set hashbestchain
        self.indexdb.set_hashbestchain(new_mainchain_hash)
            
    def get_mainchain(self):
        return self.indexdb.get_hashbestchain()
    
    def _index_transactions(self, blockhash):
        block_handle = self.get_block_handle(blockhash)
        #Add all transactions to the indexdb
        block = block_handle.get_block()
        size_blockheader = BlockheaderSerializer().get_size(block.blockheader)
        size_tx_size = VarintSerializer().get_size(len(block.transactions))
        tx_serializer = TxSerializer()
        blockpos = block_handle.blockindex.blockpos
        txpos = block_handle.blockindex.blockpos + size_blockheader + size_tx_size 
        
        for i, tx in enumerate(block.transactions):
            txindex = DbTxIndex(1, DiskTxPos(1, blockpos, txpos), [DiskTxPos() for _ in range(tx.output_count())])
            self.indexdb.set_transactionindex(hash_tx(tx), txindex)
            txpos += tx_serializer.get_size(tx)

    def _unindex_transactions(self, blockhash):
        block_handle = self.get_block_handle(blockhash)
        block = block_handle.get_block()
        for tx in block.transactions:
            self.indexdb.del_transactionindex(hash_tx(tx))   

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

    

