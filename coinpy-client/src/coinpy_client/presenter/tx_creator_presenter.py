# -*- coding:utf-8 -*-
"""
Created on 4 Mar 2012

@author: kris
"""
from coinpy.lib.bitcoin.address import is_valid_bitcoin_address
from coinpy.tools.float import is_float

class TransactionCreatorPresenter():
    def __init__(self, transaction_creator, wallet, wallet_view, messages_view):
        self.transaction_creator = transaction_creator
        self.wallet = wallet
        self.wallet_view = wallet_view
        self.messages_view = messages_view
        wallet_view.subscribe(wallet_view.EVT_SEND, self.on_send)
        #wallet_view.subscribe(wallet_view.EVT_RECEIVE, self.on_receive)
        wallet_view.sender_view.subscribe(wallet_view.sender_view.EVT_SELECT_VALUE, self.on_select_send_value)

    def on_send(self, event):
        self.wallet_view.sender_view.open()
        
    def on_select_send_value(self, event): 
        address = self.wallet_view.sender_view.address()
        amount_str = self.wallet_view.sender_view.amount() 
        if not is_valid_bitcoin_address(self.transaction_creator.runmode, address):
            self.messages_view.error("Incorrect bitcoin address: %s" % (address))
            return
        if not is_float(amount_str):
            self.messages_view.error("Incorrect amount: %s" % (amount_str))
            return
        self.transaction_creator.create_transaction(self.wallet, amount_str, float(amount_str))
        self.wallet_view.sender_view.close()
        