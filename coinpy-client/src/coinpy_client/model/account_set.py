# -*- coding:utf-8 -*-
"""
Created on 4 Mar 2012

@author: kris
"""
from coinpy.tools.observer import Observable

class AccountSet(Observable):
    EVT_ADDED_ACCOUNT = Observable.createevent()
    EVT_REMOVED_ACCOUNT = Observable.createevent()

    def __init__(self):
        super(AccountSet, self).__init__()
        self.accounts = set()
  
    def add_account(self, account):
        self.accounts.add(account)
        self.fire(self.EVT_ADDED_ACCOUNT, account=account)
        
    def remove_account(self, account):
        self.accounts.remove(account)
        self.fire(self.EVT_REMOVED_ACCOUNT, account=account)     
          
    def on_new_transaction(self, event):
        self.fire(self.EVT_NEW_TRANSACTION)
