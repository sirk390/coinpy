# -*- coding:utf-8 -*-
"""
Created on 11 Feb 2012

@author: kris
"""
from coinpy.lib.database.bsddb_env import BSDDBEnv
from coinpy.model.wallet.wallet_keypair import WalletKeypair
from coinpy.model.wallet.wallet_name import WalletName
import struct
from coinpy.lib.serialization.structures.s11n_blocklocator import BlockLocatorSerializer
from coinpy.model.wallet.wallet_poolkey import WalletPoolKey
from coinpy.lib.serialization.structures.s11n_varstr import VarstrSerializer
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.structures.s11n_wallet_tx import WalletTxSerializer
import bsddb
from coinpy.model.wallet.wallet_database_interface import WalletDatabaseInterface
from coinpy.lib.database.wallet.serialization.master_key_serializer import MasterKeySerializer

class BSDDBWalletDatabase(WalletDatabaseInterface):
    def __init__(self, bsddb_env, filename):
        self.bsddb_env = bsddb_env
        self.filename = filename
        self.varstr_serializer = VarstrSerializer()
        self.uint256_serializer = Uint256Serializer("")
        self.wallet_tx_serializer = WalletTxSerializer()
        self.master_key_serializer = MasterKeySerializer()
        self.reset_wallet()
        self.db = bsddb.db.DB(self.bsddb_env.dbenv)
        self.dbflags = bsddb.db.DB_THREAD
        
    def open(self):
        #self.bsddb_env.dbenv.fileid_reset(self.filename)
        dbtxn = self.bsddb_env.dbenv.txn_begin()
        self.db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags, txn=dbtxn)
        dbtxn.commit()
        self._read_wallet()

    def create(self):
        self.dbtxn = self.bsddb_env.dbenv.txn_begin()
        self.db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags|bsddb.db.DB_CREATE, txn=self.dbtxn)
        #create 100 pools keys, no addresses, or transactions are added
        
        self.dbtxn.commit()


    
    def begin_updates(self):
        self.dbtxn = self.bsddb_env.dbenv.txn_begin()
        
    def commit_updates(self):
        self.dbtxn.commit()
        #Synch to disk as wallet changes should not be lost
        self.db.sync()
        self.dbtxn = None

    def get_receive_key(self):
        if len(self.poolkeys) == 0:
            raise Exception("get_receive_key: No keys remaining")
        num, poolkey = next(self.poolkeys.iteritems())
        return poolkey.public_key
        
    def allocate_key(self, public_key, address, label=None, ischange=False):
        num = self.poolkeys_by_public_key[public_key].poolnum
        if num is None:
            raise Exception("allocate_pool_key: Can't find pool public_key")
        del self.poolkeys_by_public_key[public_key]
        del self.poolkeys[num]
        self.db.delete("\x04pool" + struct.pack("<q", num), txn=self.dbtxn)

        if (label and not ischange):
            self.set_label(address, label)
    
    def reset_wallet(self):
        self.master_keys = {}
        self.crypted_keys = {}
        self.keys = {}
        self.names = {}
        self.settings = []
        self.txs = {}
        self.poolkeys = {}
        self.poolkeys_by_public_key = {}
        
    def _read_entries(self, label):
        for key, value in self.db.items():
            lab, key_cursor = self.varstr_serializer.deserialize(key, 0)
            if lab == label:
                yield (key, key_cursor, value, 0)
                
    def _read_keys(self):
        for key, key_cursor, value, value_cursor in self._read_entries("key"):
            public_key, _ = self.varstr_serializer.deserialize(key, key_cursor)
            private_key, _ = self.varstr_serializer.deserialize(value, value_cursor)
            self.keys[public_key] = WalletKeypair(public_key, private_key)
    
    def _read_crypted_keys(self):
        for key, key_cursor, value, value_cursor in self._read_entries("ckey"):
            public_key, _ = self.varstr_serializer.deserialize(key, key_cursor)
            crypted_secret, _ = self.varstr_serializer.deserialize(value, value_cursor)
            self.crypted_keys[public_key] = crypted_secret

    def _read_master_keys(self):
        for key, key_cursor, value, value_cursor in self._read_entries("mkey"):
            id,  = struct.unpack_from("<I", key, key_cursor)
            self.master_keys[id], cursor = self.master_key_serializer.deserialize(value, value_cursor)

    def _read_names(self):
        for key, key_cursor, value, value_cursor in self._read_entries("name"):
            address, _ = self.varstr_serializer.deserialize(key, key_cursor)
            name, _ = self.varstr_serializer.deserialize(value, value_cursor)
            self.names[address] = WalletName(name, address)

    def _read_txs(self):
        for key, key_cursor, value, value_cursor in self._read_entries("tx"):
            hash, _ = self.uint256_serializer.deserialize(key, key_cursor)
            wallet_tx, _ = self.wallet_tx_serializer.deserialize(value, value_cursor)
            self.txs[hash] = wallet_tx

    def _read_poolkeys(self):
        for key, key_cursor, value, value_cursor in self._read_entries("pool"):
            poolnum, = struct.unpack_from("<q", key, key_cursor)
            version, = struct.unpack_from("<I", value, 0)
            time, = struct.unpack_from("<q", value, 4)
            public_key, _ = self.varstr_serializer.deserialize(value, 12)
            self.poolkeys[poolnum] = WalletPoolKey(poolnum, version, time, public_key)
            self.poolkeys_by_public_key[public_key] = self.poolkeys[poolnum]
            
    def _read_wallet(self):
        self.reset_wallet()
        self._read_keys()
        self._read_crypted_keys()
        self._read_master_keys()
        self._read_names()
        self._read_txs()
        self._read_poolkeys()
       
    def get_keys(self):
        return self.keys

    def get_crypted_keys(self):
        return self.crypted_keys

    def get_wallet_txs(self):
        return self.txs

    def get_names(self):
        return self.names
    
    def get_poolkeys(self):
        return self.poolkeys
    
    def set_label(self, address, label):
        self.names[address] = WalletName(label, address)         
        address = self.varstr_serializer.serialize(address)
        name = self.varstr_serializer.serialize(label)
        self.db.put("\x04name" + address, name, txn=self.dbtxn)

    def add_name(self, wallet_name):
        pass

    def add_keypair(self, wallet_keypair):
        pass

    def set_transaction(self, hashtx, wallet_tx):
        self.txs[hashtx] = wallet_tx
        key = self.uint256_serializer.serialize(hashtx)
        value = self.wallet_tx_serializer.serialize(wallet_tx)
        self.db.put("\x02tx" + key, value, txn=self.dbtxn)
        
    def get_transaction(self, hashtx):
        return self.txs[hashtx]

    def del_transaction(self, hashtx):
        del self.txs[hashtx]
        self.db.delete("\x02tx" + self.uint256_serializer.serialize(hashtx), txn=self.dbtxn)

    def del_poolkey(self, num):
        del self.poolkeys[num]
        self.db.delete("\x04pool" + struct.pack("<I", num))

    def get_master_keys(self):
        return (self.master_keys)

    def get_version(self):
        return (struct.unpack("<I", self.db["\x07version"])[0])

    def set_version(self, version):
        self.db["\x07version"] = struct.pack("<I", version)
    
    def get_block_locator(self):
        serializer = BlockLocatorSerializer()
        block_locator, cursor = serializer.deserialize(self.db["\x09bestblock"], 0)           
        return block_locator

    def set_blocklocator(self, blocklocator):
        serializer = BlockLocatorSerializer()
        self.db["\x09bestblock"] = serializer.serialize(blocklocator)  
    
    def __str__(self):
        keys_str = "\n".join("    " + str(k) for k in self.get_keypairs())
        pool_keys_str = "\n".join("    " + str(k) for k in self.get_poolkeys())
        names_str = "\n".join("    " + str(k) for k in self.get_names())
        tx_str = "\n".join("    " + str(k) for k in self.get_wallet_txs())
        return "Wallet\n  keys:\n" + keys_str +  "pool:\n" + pool_keys_str + "\n  names:\n" + names_str + "\n  txs:\n" + tx_str
        
if __name__ == '__main__':
    dbenv = BSDDBEnv("D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\")
    wallet = BSDDBWalletDatabase(dbenv, "wallet_testnet.dat")
    wallet.open()
    
    print wallet
    print wallet.get_version()
    print wallet.get_blocklocator()
