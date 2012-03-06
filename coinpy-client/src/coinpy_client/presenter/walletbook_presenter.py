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
from coinpy_client.presenter.wallet_presenter import WalletPresenter
from coinpy_client.presenter.tx_creator_presenter import TransactionCreatorPresenter
        #self.wallets = []           # id => Wallet
        #self.wallet_filenames = {}  # id => Wallet
        #self.dbenv_handles = {}     # directory => DBEnv

class WalletBookPresenter():
    def __init__(self, service, wallet_set, walletbook_view, messages_view): 
        self.service = service
        self.wallet_set = wallet_set
        self.walletbook_view = walletbook_view
        self.messages_view = messages_view
        self.wallet_set.subscribe(self.wallet_set.EVT_ADDED_WALLET, self.on_added_wallet)
        
    def on_added_wallet(self, event):
        wallet_balance = WalletBalance(event.wallet, self.service.blockchain)
        # add a view for the wallet
        wallet_view = self.walletbook_view.add_wallet_view(event.filename)
        # present it
        wallet_presenter = WalletPresenter(event.wallet, wallet_balance, wallet_view, self.messages_view)
        TransactionCreatorPresenter(self.service.transaction_creator, event.wallet, wallet_view, self.messages_view)
        