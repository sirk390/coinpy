# -*- coding:utf-8 -*-
"""
Created on 16 Feb 2012

@author: kris
"""
from coinpy.lib.bitcoin.wallet.wallet import Wallet
from coinpy.lib.bitcoin.blockchain.blockchain import Blockchain
from coinpy.tools.observer import Observable
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.model.constants.bitcoin import COINBASE_MATURITY

# Listens to the blockchain and the wallet and recomputes the balance accordingly
# to computer the balance, the wallet needs to know:
# the max blockheight
# the height of each transaction and if it is included in the mainchain.
class WalletBalance(Observable):
    EVT_BALANCE_CHANGED = Observable.createevent() 
    
    def __init__(self, wallet, blockchain):
        Observable.__init__(self)
        self.wallet = wallet
        self.blockchain = blockchain
        self.blockchain.subscribe(Blockchain.EVT_NEW_HIGHEST_BLOCK, self.on_new_highest_block)
        
        #get blockchain height
        self.blockchain_height = self.blockchain.get_height()
        #get heights for mainchain transactions only
        self.mainchain_outputs = []
        for tx, txout in self.wallet.iter_my_outputs():
            txhash = hash_tx(tx)
            if (self.blockchain.contains_transaction(txhash)):
                blockhandle = self.blockchain.get_transaction_handle(txhash).get_block()
                if blockhandle.is_mainchain():
                    height = self.blockchain.get_transaction_handle(txhash).get_block().get_height()
                    self.mainchain_outputs.append([height, tx, txout])
        #compute balance
        self._compute_balance()
        
    def on_new_highest_block(self, event):
        self.blockchain_height = event.height
        self._compute_balance()

    def get_confirmed(self):
        return self.confirmed

    def get_unconfirmed(self):
        return self.unconfirmed
    
    def get_height(self):
        return self.blockchain_height
    
    def _compute_balance(self):
        self.confirmed = 0
        self.unconfirmed = 0
        
        for height, tx, txout in self.mainchain_outputs:
            if (tx.iscoinbase() and (self.blockchain_height >  height + COINBASE_MATURITY)) or \
               (not tx.iscoinbase()): # set confirmed after 6 blocks here instead of 1?
                self.confirmed += txout.value
            else:
                self.unconfirmed += txout.value

        self.fire(self.EVT_BALANCE_CHANGED, confirmed=self.confirmed, unconfirmed=self.unconfirmed, height=self.blockchain_height)
        
