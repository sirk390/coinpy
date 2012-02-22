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
 
class WalletPresenter():
    def __init__(self, wallet_model, balance_model, wallet_view): 
        self.wallet_model = wallet_model
        self.balance_model = balance_model
        self.wallet_view = wallet_view
        
        #show initial data
        for key, name, poolkey in  self.wallet_model.iterkeys():
            self.wallet_view.add_key(key, poolkey, name)
        wallet_view.balance.set_balance(balance_model.get_confirmed(), balance_model.get_unconfirmed(), balance_model.get_height())
        #subscribe to events for further modifications
        balance_model.subscribe(balance_model.EVT_BALANCE_CHANGED, self.on_balance_changed)
        
    def on_balance_changed(self, event):
        self.wallet_view.balance.set_balance( event.confirmed, event.unconfirmed, event.height)


