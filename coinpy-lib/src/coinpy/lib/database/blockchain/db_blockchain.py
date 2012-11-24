from coinpy.lib.database.blockchain.block_storage import BlockStorage
from coinpy.model.protocol.structures.uint256 import Uint256
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
        genesis_index = DbBlockIndex(self.version, Uint256.zero(), file, blockpos, 0, genesis_block.blockheader)
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

    def get_next_in_mainchain(self, blockhash):
        if not self.indexdb.contains_block(blockhash):
            return None
        blockindex = self.indexdb.get_blockindex(blockhash)
        if (blockindex.hash_next == Uint256.zero()):
            return None
        return blockindex.hash_next
    
    def append_block(self, blockhash, block):
        file, blockpos = self.blockstore.saveblock(block)
        prevblock = self.get_block_handle(block.blockheader.hash_prev)
        
        idx = DbBlockIndex(self.version, Uint256.zero(), file, blockpos, prevblock.get_height()+1, block.blockheader)
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
        while hash != Uint256.zero():
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

    def reorganize(self, reorganize_update):
        old_afterfork_hash, old_afterfork_block = reorganize_update.old_mainchain[0]
        new_mainchain_besthash, new_mainchain_bestblock = reorganize_update.new_mainchain[-1]
        hashfork = old_afterfork_block.blockheader.hash_prev
        #Unindex transactions in old mainchain
        for hash, blk in reorganize_update.old_mainchain:
            blkindex = self.indexdb.get_blockindex(hash)
            self._unindex_transactions(hash)
        #Set hash_next to 0 in old mainchain
        for hash, blk in reorganize_update.old_mainchain:
            blkindex = self.indexdb.get_blockindex(hash)
            blkindex.hash_next = Uint256.zero()
            self.indexdb.set_blockindex(hash, blkindex)
        #Remove the blocks of the old mainchain    
        for hash, blk in reorganize_update.old_mainchain:
            pass #self.append_block(hash, blk)
        #Add the blocks of the new mainchain    
        for hash, blk in reorganize_update.new_mainchain:
            self.append_block(hash, blk)
        #Index transactions in new mainchain    
        for hash, blk in reorganize_update.new_mainchain:
            self._index_transactions(hash)
        #Set hash_next to 'next' in new mainchain
        next = Uint256.zero()
        for hash, blkindex in reversed(reorganize_update.new_mainchain):
            blkindex = self.indexdb.get_blockindex(hash)
            blkindex.hash_next = next
            self.indexdb.set_blockindex(hash, blkindex)
            next = hash
        #set next of fork
        blkindex = self.indexdb.get_blockindex(hashfork)
        blkindex.hash_next = next
        self.indexdb.set_blockindex(hashfork, blkindex)
        #set hashbestchain
        self.indexdb.set_hashbestchain(new_mainchain_besthash)

    def is_mainchain(self, hash):
        pass
            
    def get_mainchain(self):
        return self.indexdb.get_hashbestchain()
    
    def get_genesis(self):
        return self.genesishash
    
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
    from coinpy.model.protocol.structures.uint256 import Uint256
    print db.indexdb.hashbestchain()
    print db.contains_block(Uint256.from_hexstr("00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048"))
    print db.contains_block(Uint256.from_hexstr("00000000139a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048"))
    it = db.get_block_iterator(Uint256.from_hexstr("000000000000029b4b03122dc75e22952e574ded1ba7caef1fd81c1d11f08e73"))
    print it.get_block()
    print db.indexdb.hashbestchain()
    print db.get_block_iterator(db.indexdb.hashbestchain())
    
    #
    print db.contains_transaction(Uint256.from_hexstr("f8780c27a0af1eb62968a5ab20417f706706f3fa7316775ae0f59850bb757c72"))
    print db.get_transaction_iterator(Uint256.from_hexstr("f8780c27a0af1eb62968a5ab20417f706706f3fa7316775ae0f59850bb757c72"))
    it = db.get_transaction_iterator(Uint256.from_hexstr("f8780c27a0af1eb62968a5ab20417f706706f3fa7316775ae0f59850bb757c72"))
    
    print db.get_block_iterator(db.indexdb.hashbestchain()).get_block()
    #db.addblock("hello")
    #db.load_owner_transactions(owner1)
    #print db.load_txindex(Uint256.from_hexstr("00004b78031f6f406c23cb7d1d0990d56f39107febe8c982a5f75a87254143ea"))

    

