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
from coinpy.tools.bitcoin.base58check import verify_base58check
from coinpy.lib.bitcoin.address import is_valid_bitcoin_address
from coinpy.tools.float import is_float
from coinpy.model.constants.bitcoin import COIN
 
class AccountPresenter():
    def __init__(self, account, wallet_view, messages_view): 
        self.account = account
        #self.balance = wallet_manager.balance
        self.wallet_view = wallet_view
        self.messages_view = messages_view
        
        #show account balance
        for key, name, poolkey in  self.account.wallet.iterkeys():
            self.wallet_view.add_key(key.public_key, key, poolkey, name)
        wallet_view.balance.set_balance(account.get_confirmed_balance(), account.get_unconfirmed_balance(), account.get_blockchain_height())
        #show transaction history
        for wallet_tx, hash, date, address, name, amount, confirmed in self.account.iter_transaction_history():
            self.wallet_view.add_transaction_history_item(hash, date, address, name, amount, confirmed)
        #listen to balance updates
        self.account.subscribe(self.account.EVT_BALANCE_CHANGED, self.on_balance_changed)
        self.account.subscribe(self.account.EVT_NEW_TRANSACTION_ITEM, self.on_new_transaction_item)
        self.account.subscribe(self.account.EVT_CONFIRMED_TRANSACTION_ITEM, self.on_confirmed_transaction_item)
        self.account.subscribe(self.account.EVT_NEW_ADDRESS_LABEL, self.on_new_address_label)
                               
        wallet_view.subscribe(wallet_view.EVT_SEND, self.on_send)
        wallet_view.subscribe(wallet_view.EVT_RECEIVE, self.on_receive)
        
        wallet_view.send_view.subscribe(wallet_view.send_view.EVT_SELECT_VALUE, self.on_select_send_value)
        wallet_view.receive_view.subscribe(wallet_view.receive_view.EVT_SET_LABEL, self.on_set_receive_label)



    def close(self):
        self.account.unsubscribe(self.account.EVT_BALANCE_CHANGED, self.on_balance_changed)
        
    def on_balance_changed(self, event):
        self.wallet_view.balance.set_balance( event.confirmed, event.unconfirmed, event.height)

    def on_new_transaction_item(self, event):
        tx, hash, date, address, name, amount, confirmed = event.item
        self.wallet_view.add_transaction_history_item(hash, date, address, name, amount, confirmed)
    
    def on_confirmed_transaction_item(self, event):
        txhash, = event.item
        self.wallet_view.set_confirmed(txhash, True)
    
    def on_new_address_label(self, event):
        self.wallet_view.set_key_label(event.public_key, event.address, event.label)
        self.wallet_view.select_key(event.public_key)
        
    def on_send(self, event):
        self.wallet_view.send_view.open()

    
    def on_receive(self, event):
        receive_address = self.account.get_receive_address()
        self.wallet_view.receive_view.set_receive_address(receive_address)
        self.wallet_view.receive_view.open()
    
    def on_set_receive_label(self, event):
        receive_address = self.wallet_view.receive_view.get_receive_address()
        label = self.wallet_view.receive_view.get_label()
        self.account.set_receive_label(receive_address, label)
        
    def on_select_send_value(self, event): 
        address = self.wallet_view.send_view.address()
        amount_str = self.wallet_view.send_view.amount() 
        if not is_valid_bitcoin_address(self.account.wallet.runmode, address):
            self.messages_view.error("Incorrect bitcoin address: %s" % (address))
            return
        if not is_float(amount_str):
            self.messages_view.error("Incorrect amount: %s" % (amount_str))
            return
        self.account.send_transaction(int(float(amount_str) * COIN), address, 0)
        self.wallet_view.send_view.close()
    
if __name__ == '__main__':
    #n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo
    import wx
    from coinpy_client.view.wallet.wallet_panel import WalletPanel
    from coinpy.lib.database.bsddb_env import BSDDBEnv
    from coinpy_tests.mock import Mock
    from coinpy.model.protocol.runmode import MAIN, TESTNET
    from coinpy_client.view.message_view import MessageView

    runmode = TESTNET
    wallet_filename= "D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\wallet_testnet.dat"
    
    directory, filename = os.path.split(wallet_filename)
    
    bsddb_env = BSDDBEnv(directory)
    wallet = Wallet(None, BSDDBWalletDatabase(bsddb_env, filename), runmode)
    balance = Mock({"get_confirmed" : 175877, "get_unconfirmed" : 2828727, "get_height" : 3}, accept_all_methods=True)
    
    wallet_account = Mock(attributes={})
    
    app = wx.App(False)
    frame = wx.Frame(None, size=(600,500))
    wallet_view = WalletPanel(None, frame)
    AccountPresenter(wallet_account, wallet_view, MessageView(None))
    
    frame.Show()
    app.MainLoop()


