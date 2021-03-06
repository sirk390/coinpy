from coinpy.model.blockchain.tx_handle import TxHandle
from coinpy.lib.blocks.hash_block import hash_blockheader
from coinpy.lib.blockchain.bsddb.db_blockhandle import DBBlockHandle
from coinpy.lib.transactions.hash_tx import hash_tx
import warnings

class DBTxHandle(TxHandle):
    def __init__(self, log, indexdb, blockstorage, hash):
        self.log = log
        self.indexdb = indexdb
        self.txindex = self.indexdb.get_transactionindex(hash)
        self.blockstorage = blockstorage
        self.hash = hash
        
    def get_transaction(self):
        return (self.blockstorage.load_tx(self.txindex.pos.file, self.txindex.pos.txpos))

    def get_block_hash(self):
        blockheader = self.blockstorage.load_blockheader(self.txindex.pos.file, self.txindex.pos.blockpos)
        return hash_blockheader(blockheader)
        
    def get_block(self):
        warnings.warn("deprecated", DeprecationWarning)
        return DBBlockHandle(self.log, self.indexdb, self.blockstorage, self.get_block_hash())
        
    def is_output_spent(self, output):
        return (not self.txindex.spent[output].isnull())

    def get_spending_transactionu_hash(self, n):
        disktxpos = self.txindex.spent[n]
        tx = self.blockstorage.load_tx(disktxpos.file, disktxpos.txpos)
        return hash_tx(tx)
    
    def get_spending_transaction(self, n):
        warnings.warn("deprecated", DeprecationWarning)
        return DBTxHandle(self.log, self.indexdb, self.blockstorage, self.get_spending_transactionu_hash(n))
        
    def output_count(self):
        return (len(self.txindex.spent))
    
    def mark_spent(self, n, is_spent, in_tx_hash=None):
        if (is_spent):   
            spent_txindex = self.indexdb.get_transactionindex(in_tx_hash)
            self.txindex.spent[n] = spent_txindex.pos
        else:
            self.txindex.spent[n].setnull()
        self.indexdb.set_transactionindex(self.hash, self.txindex)
