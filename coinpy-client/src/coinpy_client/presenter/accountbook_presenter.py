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
        
    def on_added_account(self, event):
        account = event.account
        #wallet_balance = WalletBalance(event.wallet, self.service.blockchain)
        # add a view for the wallet
        wallet_view = self.walletbook_view.add_wallet_view(account.name)
        # present it
        wallet_presenter = AccountPresenter(event.account, wallet_view, self.messages_view)
        #TransactionCreatorPresenter(self.service.transaction_creator, event.wallet, wallet_view, self.messages_view)
        