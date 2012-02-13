# -*- coding:utf-8 -*-
"""
Created on 11 Feb 2012

@author: kris
"""
from coinpy.lib.database.bsddb_env import BsdDbEnv
from coinpy.model.wallet.wallet_tx import WalletTx
from coinpy.model.wallet.wallet_keypair import WalletKeypair
from coinpy.model.wallet.wallet_name import WalletName
import struct
from coinpy.lib.serialization.structures.s11n_blocklocator import BlockLocatorSerializer
from coinpy.model.wallet.wallet_poolkey import WalletPoolKey
from coinpy.lib.serialization.structures.s11n_varstr import VarstrSerializer
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer

class WalletDatabase():
    def __init__(self, bsddb_env, filename):
       
        self.varstr_serializer = VarstrSerializer()
        self.uint256_serializer = Uint256Serializer("")
        self.tx_serializer = TxSerializer()
        self.reset_wallet()
        
    def open(self):
        #BsdDbBase.open(self)
        self._read_wallet()
    
    def reset_wallet(self):
        self.keys = {}
        self.names = {}
        self.settings = []
        self.txs = {}
        self.pool = {}
    
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
    
    def _read_names(self):
        for key, key_cursor, value, value_cursor in self._read_entries("name"):
            address, _ = self.varstr_serializer.deserialize(key, key_cursor)
            name, _ = self.varstr_serializer.deserialize(value, value_cursor)
            self.names[address] = WalletName(name, address)

    def _read_txs(self):
        for key, key_cursor, value, value_cursor in self._read_entries("tx"):
            hash, _ = self.uint256_serializer.deserialize(key, key_cursor)
            tx, _ = self.tx_serializer.deserialize(value, value_cursor)
            self.txs[hash] = WalletTx(hash, tx)

    def _read_poolkeys(self):
        for key, key_cursor, value, value_cursor in self._read_entries("pool"):
            poolnum, = struct.unpack_from("<I", key, key_cursor)
            version, = struct.unpack_from("<I", value, 0)
            time, = struct.unpack_from("<q", value, 4)
            hash, _ = self.uint256_serializer.deserialize(value, 12)
            self.pool[poolnum] = WalletPoolKey(poolnum, version, time, hash)
        
    def _read_wallet(self):
        self.reset_wallet()
        self._read_keys()
        self._read_names()
        self._read_txs()
        self._read_poolkeys()
       
    def get_keypairs(self):
        return self.keypairs

    def get_names(self):
        return self.names
    
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
        keys_str = "\n".join("    " + str(k) for k in self.keys.values())
        pool_keys_str = "\n".join("    " + str(k) for k in self.pool.values())
        names_str = "\n".join("    " + str(k) for k in self.names.values())
        tx_str = "\n".join("    " + str(k) for k in self.txs.values())
        return "Wallet\n  keys:\n" + keys_str +  "pool:\n" + pool_keys_str + "\n  names:\n" + names_str + "\n  txs:\n" + tx_str
        
if __name__ == '__main__':
    wallet = WalletDatabase("D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\", "wallet_testnet.dat")
    wallet.open()
    print wallet
    print wallet.get_version()
    print wallet.get_blocklocator()
