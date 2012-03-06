# -*- coding:utf-8 -*-
"""
Created on 4 Mar 2012

@author: kris
"""
from coinpy.tools.observer import Observable
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.lib.bitcoin.wallet.wallet import Wallet
from coinpy.lib.bitcoin.wallet.wallet_balance import WalletBalance


class WalletSet(Observable):
    EVT_ADDED_WALLET = Observable.createevent()
    EVT_NEW_TRANSACTION = Observable.createevent()
    #TODO (someday): remove blockchain dependency.
    def __init__(self, blockchain, runmode):
        super(WalletSet, self).__init__()
        self.blockchain = blockchain
        self.runmode = runmode
        self.wallets = []           # id => Wallet
        self.wallet_filenames = {}  # id => Wallet
        
    def open_wallet(self, dbenv, filename):
        wallet_db = BSDDBWalletDatabase(dbenv, filename)
        wallet = Wallet(wallet_db, self.runmode)
        self.wallets.append(wallet)
        self.wallet_filenames[wallet] = filename
        
        self.fire(self.EVT_ADDED_WALLET, wallet=wallet, filename=filename)
    
        wallet.subscribe(wallet.EVT_NEW_TRANSACTION, self.on_new_transaction)

    def on_new_transaction(self, event):
        self.fire(self.EVT_NEW_TRANSACTION)
