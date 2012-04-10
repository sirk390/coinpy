# -*- coding:utf-8 -*-
"""
Created on 12 Mar 2012

@author: kris
"""

class Account():
    def iter_my_outputs(self):
        pass
    def iter_transaction_history(self):
        pass
    def iter_unconfirmed_transactions(self):
        pass
    def get_balance(self):
        #coins seen in mainchain at a depth of 6
        pass
    def get_unconfirmed_balance(self):
        #minted coins < COINBASE_MATURITY + received coins <6
        pass
    def get_besthash(self): 
        pass
    def set_coin_selector(self, coin_selector):
        pass
    def send_transaction(self, amount, address, fee):
        pass
