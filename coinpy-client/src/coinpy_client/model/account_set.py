# -*- coding:utf-8 -*-
"""
Created on 4 Mar 2012

@author: kris
"""
from coinpy.tools.observer import Observable
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.lib.bitcoin.wallet.wallet import Wallet
from coinpy.lib.bitcoin.wallet.wallet_balance import WalletBalance


class AccountSet(Observable):
    EVT_ADDED_ACCOUNT = Observable.createevent()
    EVT_REMOVED_ACCOUNT = Observable.createevent()
    #EVT_NEW_TRANSACTION = Observable.createevent()
    #TODO (someday): remove blockchain dependency.
    def __init__(self, reactor):
        super(AccountSet, self).__init__(reactor)
        self.wallet_managers = []           # id => Wallet
        self.wallet_filenames = {}  # id => Wallet
        self.accounts = set()
    """    
    def open_wallet(self, dbenv, filename):
        wallet_db = BSDDBWalletDatabase(dbenv, filename)
        wallet = Wallet(wallet_db, self.runmode)
        wallet_manager = WalletManager(wallet, self.blockchain, self.node)
        self.wallet_managers.append(wallet_manager)
        self.wallet_filenames[wallet] = filename
        
        self.fire(self.EVT_ADDED_WALLET, wallet_manager=wallet_manager, filename=filename)
    """
    def add_account(self, account):
        self.accounts.add(account)
        self.fire(self.EVT_ADDED_ACCOUNT, account=account)
        
    def remove_account(self, account):
        self.accounts.remove(account)
        self.fire(self.EVT_REMOVED_ACCOUNT, account=account)     
          
    def on_new_transaction(self, event):
        self.fire(self.EVT_NEW_TRANSACTION)
