# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from coinpy.lib.database.bsddb_env import BSDDBEnv
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY
from coinpy.lib.script.standard_script_tools import tx_pubkeyhash_get_address,\
    identify_script, tx_pubkey_get_pubkey
from coinpy.tools.bitcoin.hash160 import hash160
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.tools.bitcoin.base58 import b58encode
from coinpy.model.constants.bitcoin import COIN

class Wallet():
    def __init__(self, wallet_database):
        self.wallet_database = wallet_database
        self.wallet_database.open()
        
        self.addresses = {}
        for keypair in self.wallet_database.get_keypairs():
            self.addresses[hash160(keypair.public_key)] = keypair
    
    def get_keys(self):
        return self.wallet_database.keypairs
    
    def have_key_for_addresss(self, address):
        return (address in self.addresses)

    def have_key(self, pubkey):
        pass
    
    def is_mine(self, txout):
        script_type = identify_script(txout.script)
        #if unknown script type, return False
        if (script_type is None): 
            return False 
        if script_type == TX_PUBKEYHASH:
            address = tx_pubkeyhash_get_address(txout.script)
            return self.have_key_for_addresss(address)
        if script_type == TX_PUBKEY:
            address = hash160(tx_pubkey_get_pubkey(txout.script))
            return self.have_key_for_addresss(address) # todo:replace with have_key
        return False 
    
    def is_change(self, txout): 
        #current assumption is that any payment to a TX_PUBKEYHASH that is mine but isn't in the address book is change. 
        pass
   
    def get_balance(self):
        #TODO: compute immature minted / unconfirmed transfered
        balance = 0
        for hash, tx in self.wallet_database.get_wallet_txs().iteritems():
            for index, txout in enumerate(tx.merkle_tx.tx.out_list):
                if not tx.is_spent(index) and self.is_mine(txout):
                    balance += txout.value
        return balance


if __name__ == '__main__':
    dbenv = BSDDBEnv("D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\")
    wallet_db = BSDDBWalletDatabase(dbenv, "wallet_testnet.dat")
    wallet = Wallet(wallet_db)
    
    print wallet.get_balance() * 1.0 / COIN 
        
    