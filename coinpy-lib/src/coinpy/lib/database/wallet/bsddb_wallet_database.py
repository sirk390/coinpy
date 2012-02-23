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

class BSDDBWalletDatabase(WalletDatabaseInterface):
    def __init__(self, bsddb_env, filename):
        self.bsddb_env = bsddb_env
        self.filename = filename
        self.varstr_serializer = VarstrSerializer()
        self.uint256_serializer = Uint256Serializer("")
        self.wallet_tx_serializer = WalletTxSerializer()
        self.reset_wallet()
        self.db = bsddb.db.DB(self.bsddb_env.dbenv)
        self.dbflags = bsddb.db.DB_THREAD
        
    def open(self):
        dbtxn = self.bsddb_env.dbenv.txn_begin()
        self.db.open(self.filename, "main", bsddb.db.DB_BTREE, self.dbflags, txn=dbtxn)
        dbtxn.commit()
        self._read_wallet()
    
    def reset_wallet(self):
        self.keypairs = {}
        self.names = {}
        self.settings = []
        self.txs = {}
        self.poolkeys = {}
    
    def _read_entries(self, label):
        for key, value in self.db.items():
            lab, key_cursor = self.varstr_serializer.deserialize(key, 0)
            if lab == label:
                yield (key, key_cursor, value, 0)
                
    def _read_keys(self):
        for key, key_cursor, value, value_cursor in self._read_entries("key"):
            public_key, _ = self.varstr_serializer.deserialize(key, key_cursor)
            private_key, _ = self.varstr_serializer.deserialize(value, value_cursor)
            self.keypairs[public_key] = WalletKeypair(public_key, private_key)
    
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
            poolnum, = struct.unpack_from("<I", key, key_cursor)
            version, = struct.unpack_from("<I", value, 0)
            time, = struct.unpack_from("<q", value, 4)
            public_key, _ = self.varstr_serializer.deserialize(value, 12)
            self.poolkeys[poolnum] = WalletPoolKey(poolnum, version, time, public_key)
        
    def _read_wallet(self):
        self.reset_wallet()
        self._read_keys()
        self._read_names()
        self._read_txs()
        self._read_poolkeys()
       
    def get_keypairs(self):
        return self.keypairs.values()

    def get_wallet_txs(self):
        return self.txs

    def get_names(self):
        return self.names
    
    def get_poolkeys(self):
        return self.poolkeys
    
    def begin_updates(self):
        pass

    def commit_updates(self):
        pass

    def add_name(self, wallet_name):
        pass

    def add_keypair(self, wallet_keypair):
        pass
    
    def get_version(self):
        return (struct.unpack("<I", self.db["\x07version"])[0])

    def set_version(self, version):
        self.db["\x07version"] = struct.pack("<I", version)
    
    def get_blocklocator(self):
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
