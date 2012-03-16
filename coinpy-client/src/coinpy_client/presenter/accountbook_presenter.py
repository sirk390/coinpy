# -*- coding:utf-8 -*-
"""
Created on 21 Feb 2012

@author: kris
"""
#wallets
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.lib.bitcoin.wallet.wallet import Wallet
from coinpy.lib.bitcoin.wallet.wallet_balance import WalletBalance
import os
from coinpy_client.presenter.tx_creator_presenter import TransactionCreatorPresenter
from coinpy_client.presenter.account_presenter import AccountPresenter
        #self.wallets = []           # id => Wallet
        #self.wallet_filenames = {}  # id => Wallet
        #self.dbenv_handles = {}     # directory => DBEnv

class AccountBookPresenter():
    def __init__(self, service, account_set, walletbook_view, messages_view): 
        self.service = service
        self.account_set = account_set
        self.walletbook_view = walletbook_view
        self.messages_view = messages_view
        self.account_set.subscribe(self.account_set.EVT_ADDED_ACCOUNT, self.on_added_account)
        self.account_set.subscribe(self.account_set.EVT_REMOVED_ACCOUNT, self.on_removed_account)
        
        self.walletbook_view.subscribe(self.walletbook_view.EVT_CLOSE_WALLET, self.on_close_account_view)
       
        self.account_presenters = {}
        
    def on_added_account(self, event):
        # add a view for the wallet
        wallet_view = self.walletbook_view.add_wallet_view(event.account, event.account.name)
        # present it
        wallet_presenter = AccountPresenter(event.account, wallet_view, self.messages_view)
        self.account_presenters[event.account] = wallet_presenter

    def on_removed_account(self, event):
        del self.account_presenters[event.account]
        self.walletbook_view.remove_wallet_view(event.account)
    
    def on_close_account_view(self, event):
        #stop presenting
        self.account_presenters[event.id].close()
        #removed view
        self.account_set.remove_account(event.id)
            