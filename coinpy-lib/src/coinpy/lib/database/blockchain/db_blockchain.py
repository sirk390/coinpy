# -*- coding:utf-8 -*-
"""
Created on 25 Jul 2011

@author: kris
"""

from coinpy.lib.database.blockchain.block_storage import BlockStorage
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.database.blockchain.objects.blockindex import DbBlockIndex
from coinpy.model.protocol.runmode import MAIN
from coinpy.lib.database.blockchain.indexdb import IndexDB
from coinpy.lib.bitcoin.hash_block import hash_block
from coinpy.model.blockchain.blockchain_database import BlockChainDatabase
from coinpy.lib.database.blockchain.db_blockhandle import DBBlockHandle
from coinpy.lib.database.blockchain.db_txhandle import DBTxHandle
from coinpy.lib.database.blockchain.objects.txindex import DbTxIndex
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.lib.database.blockchain.objects.disktxpos import DiskTxPos
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer
from coinpy.model.genesis import GENESIS

class BSDDbBlockChainDatabase(BlockChainDatabase):
    def __init__(self, log, bdsdb_env, runmode):
        self.log = log
        self.runmode = runmode
        self.indexdb = IndexDB(runmode, bdsdb_env)
        self.blockstore = BlockStorage(runmode, bdsdb_env.directory)
        self.version = 32200
        self.genesishash = None
        self.genesisblock = None

    def open(self):
        self.indexdb.open()
    
    def exists(self):
        return (self.indexdb.exists())

    def create(self, genesis_block):
        file, blockpos = self.blockstore.saveblock(genesis_block)
        self.blockstore.commit()
        genesis_index = DbBlockIndex(self.version, uint256.zero(), file, blockpos, 0, genesis_block.blockheader)
        self.indexdb.create(hash_block(genesis_block), genesis_index)
    
    def open_or_create(self, genesisblock):
        self.genesisblock = genesisblock
        self.genesishash = hash_block(genesisblock)
       
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
        
        idx = DbBlockIndex(self.version, uint256.zero(), file, blockpos, prevblock.get_height()+1, block.blockheader)
        self.indexdb.set_blockindex(blockhash, idx)
        if prevblock.hash == self.get_mainchain():
            prevblock.blockindex.hash_next = blockhash
            self.indexdb.set_blockindex(prevblock.hash, prevblock.blockindex)
            self.indexdb.set_hashbestchain(blockhash)
            self._index_transactions(blockhash, block)
        return DBBlockHandle(self.log, self.indexdb, self.blockstore, blockhash, block=block)

    """
        Mainchain Operations
    """    
    def _find_fork(self, altchainhash):
        hash = altchainhash
        while hash != uint256.zero():
            handle = self.get_block_handle(hash)
            if handle.is_mainchain():
                return hash
            hash = handle.get_blockheader().hash_prev 
        return handle.hash
    
    # iterate backwards in [hashfirst-hashlast] and yield (hash, blkindex)
    def _iterate_branch(self, hashfirst, hashlast):
        hash = hashlast
        while (hash != hashfirst):
            blockindex = self.indexdb.get_blockindex(hash)
            yield (hash, blockindex)
            hash = blockindex.blockheader.hash_prev
        
    def set_mainchain(self, new_mainchain_hash):
        hashfork = self._find_fork(new_mainchain_hash)
        #set hash_next to 0 in previous mainchain and unindex transactions
        for hash, blkindex in self._iterate_branch(hashfork, self.indexdb.get_hashbestchain()):
            blkindex.hash_next = uint256.zero()
            self.indexdb.set_blockindex(hash, blkindex)
            self._unindex_transactions(hash)
        #set hash_next to next in new mainchain and index transactions
        next = uint256.zero()
        for hash, blkindex in self._iterate_branch(hashfork, new_mainchain_hash):
            blkindex.hash_next = next
            self.indexdb.set_blockindex(hash, blkindex)
            next = hash
            self._index_transactions(hash)
        #set next of fork
        blkindex = self.indexdb.get_blockindex(hashfork)
        blkindex.hash_next = next
        self.indexdb.set_blockindex(hashfork, blkindex)
        #set hashbestchain
        self.indexdb.set_hashbestchain(new_mainchain_hash)

    def is_mainchain(self, hash):
        pass
            
    def get_mainchain(self):
        return self.indexdb.get_hashbestchain()
    
    def _index_transactions(self, blockhash, block=None):
        block_handle = self.get_block_handle(blockhash)
        #Add all transactions to the indexdb
        if not block:
            block = block_handle.get_block()
        size_blockheader = BlockheaderSerializer().get_size(block.blockheader)
        size_tx_size = VarintSerializer().get_size(len(block.transactions))
        tx_serializer = TxSerializer()
        blockpos = block_handle.blockindex.blockpos
        txpos = block_handle.blockindex.blockpos + size_blockheader + size_tx_size 
        
        for i, tx in enumerate(block.transactions):
            txindex = DbTxIndex(1, DiskTxPos(1, blockpos, txpos), [DiskTxPos() for _ in range(tx.output_count())])
            self.indexdb.set_transactionindex(hash_tx(tx), txindex)
            #TODO: speed this up...
            if tx.rawdata:
                txpos += len(tx.rawdata)
            else:
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

    

