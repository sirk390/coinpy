# -*- coding:utf-8 -*-
"""
Created on 19 Apr 2012

@author: kris
"""

import unittest
from coinpy.lib.database.bsddb_env import BSDDBEnv
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.tools.hex import hexstr

class TestWalletDatabase(unittest.TestCase):
    def setUp(self):
        self.dbenv = BSDDBEnv(".")
    """    
    def test_wallet_database(self):
        wallet = BSDDBWalletDatabase(self.dbenv, "wallet_unencrypted.dat")
        wallet.open()
        #keys, names, tx, pool
        str(wallet)
        wallet.get_version()
        wallet.get_blocklocator()
    """ 
    def test_wallet_database_encrypted(self):
        wallet = BSDDBWalletDatabase(self.dbenv, "wallet_encrypted_hello.dat")
        wallet.open()
        print wallet.get_master_keys()
        for public_key, crypted_secret in  wallet.crypted_keys.iteritems():
            print "public_key", hexstr(public_key)
            print "crypted_secret", hexstr(crypted_secret)
        #keys, names, tx, pool
        #print wallet.db.keys()
        

if __name__ == '__main__':
    unittest.main()
          