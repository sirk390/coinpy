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
 
class WalletPresenter():
    def __init__(self, wallet_model, balance_model, wallet_view, messages_view): 
        self.wallet_model = wallet_model
        self.balance_model = balance_model
        self.wallet_view = wallet_view
        self.messages_view = messages_view
        
        #show wallet balance
        for key, name, poolkey in  self.wallet_model.iterkeys():
            self.wallet_view.add_key(key, poolkey, name)
        wallet_view.balance.set_balance(balance_model.get_confirmed(), balance_model.get_unconfirmed(), balance_model.get_height())
        #show transaction history
        for date, address, name, amount in self.wallet_model.iter_transaction_history():
            self.wallet_view.add_transaction_history_item(date, address, name, amount)
        #listen to balance updates
        balance_model.subscribe(balance_model.EVT_BALANCE_CHANGED, self.on_balance_changed)
        #listen to view send/receive
        wallet_view.subscribe(wallet_view.EVT_SEND, self.on_send)
        wallet_view.subscribe(wallet_view.EVT_RECEIVE, self.on_receive)
        wallet_view.sender_view.subscribe(wallet_view.sender_view.EVT_SELECT_VALUE, self.on_select_send_value)

    def on_send(self, event):
        self.wallet_view.sender_view.open()
        
    def on_select_send_value(self, event): 
        address = self.wallet_view.sender_view.address()
        amount_str = self.wallet_view.sender_view.amount() 
        if not is_valid_bitcoin_address(self.wallet_model.runmode, address):
            self.messages_view.error("Incorrect bitcoin address: %s" % (address))
            return
        #FIXME: clean check for float + money range + balance
        try:
            amount = float(amount_str)
        except:
            self.messages_view.error("Incorrect amount: %s" % (amount_str))
            return
        self.wallet_view.sender_view.close()
        
    def on_receive(self, event):
        pass
    
        
    def on_balance_changed(self, event):
        self.wallet_view.balance.set_balance( event.confirmed, event.unconfirmed, event.height)

if __name__ == '__main__':
    #n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo
    import wx
    from coinpy_client.gui.view.wallet.wallet_panel import WalletPanel
    from coinpy.lib.database.bsddb_env import BSDDBEnv
    from coinpy_tests.mock import Mock
    from coinpy.model.protocol.runmode import MAIN, TESTNET
    from coinpy_client.gui.view.message_view import MessageView

    runmode = TESTNET
    wallet_filename= "D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\wallet_testnet.dat"
    
    directory, filename = os.path.split(wallet_filename)
    
    bsddb_env = BSDDBEnv(directory)
    wallet = Wallet(BSDDBWalletDatabase(bsddb_env, filename), runmode)
    balance_model = Mock({"get_confirmed" : 175877, "get_unconfirmed" : 2828727, "get_height" : 3}, accept_all_methods=True)
    
    app = wx.App(False)
    frame = wx.Frame(None, size=(600,500))
    wallet_view = WalletPanel(frame)
    WalletPresenter(wallet, balance_model, wallet_view, MessageView(None))
    
    frame.Show()
    app.MainLoop()


