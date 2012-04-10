# -*- coding:utf-8 -*-
"""
Created on 4 Mar 2012

@author: kris
"""
# TransactionPublisher
#     Puts transactions in the wallet, relays unconfirmed wallet transactions to
#     the node trickler. 
class TransactionPublisher():
    # transaction_source: wallet or wallet_set
    def __init__(self, reactor, node, wallet_set):
        self.reactor = reactor
        self.wallet_set = wallet_set
        self.transaction_source.subscribe(self.transaction_source.EVT_NEW_TRANSACTION, self.on_new_transaction)
    
    def on_new_transaction(self, transaction):
        print "new transaction", str(transaction)
    
    def send_transaction(self, tx):
        pass
    