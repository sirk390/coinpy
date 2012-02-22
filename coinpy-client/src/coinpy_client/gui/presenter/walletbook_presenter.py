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
from coinpy_client.gui.presenter.wallet_presenter import WalletPresenter
        #self.wallets = []           # id => Wallet
        #self.wallet_filenames = {}  # id => Wallet
        #self.dbenv_handles = {}     # directory => DBEnv

class WalletBookPresenter():
    def __init__(self, service, walletbook_view): 
        self.service = service
        self.walletbook_view = walletbook_view
        self.wallets = []           # id => Wallet
        self.wallet_filenames = {}  # id => Wallet
    
    def open_wallet(self, dbenv, filename):
        wallet_db = BSDDBWalletDatabase(dbenv, filename)
        wallet = Wallet(wallet_db, self.service.nodeparams.runmode)
        wallet_balance = WalletBalance(wallet, self.service.blockchain)
        self.wallets.append(wallet)
        self.wallet_filenames[wallet] = filename
        # add a view for the wallet
        wallet_view = self.walletbook_view.add_wallet_view(filename)
        # present it
        wallet_presenter = WalletPresenter(wallet, wallet_balance, wallet_view)
