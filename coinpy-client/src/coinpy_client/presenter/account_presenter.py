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
 
class AccountPresenter():
    def __init__(self, account, wallet_view, messages_view): 
        self.account = account
        #self.balance = wallet_manager.balance
        self.wallet_view = wallet_view
        self.messages_view = messages_view
        
        #show account balance
        for key, name, poolkey in  self.account.wallet.iterkeys():
            self.wallet_view.add_key(key, poolkey, name)
        wallet_view.balance.set_balance(account.get_confirmed_balance(), account.get_unconfirmed_balance(), account.get_blockchain_height())
        #show transaction history
        for date, address, name, amount in self.account.iter_transaction_history():
            self.wallet_view.add_transaction_history_item(date, address, name, amount)
        #listen to balance updates
        self.account.subscribe(self.account.EVT_BALANCE_CHANGED, self.on_balance_changed)


        wallet_view.subscribe(wallet_view.EVT_SEND, self.on_send)
        wallet_view.sender_view.subscribe(wallet_view.sender_view.EVT_SELECT_VALUE, self.on_select_send_value)

    def close(self):
        self.account.unsubscribe(self.account.EVT_BALANCE_CHANGED, self.on_balance_changed)
        
    def on_balance_changed(self, event):
        self.wallet_view.balance.set_balance( event.confirmed, event.unconfirmed, event.height)

    def on_send(self, event):
        self.wallet_view.sender_view.open()
        
    def on_select_send_value(self, event): 
        address = self.wallet_view.sender_view.address()
        amount_str = self.wallet_view.sender_view.amount() 
        if not is_valid_bitcoin_address(self.account.wallet.runmode, address):
            self.messages_view.error("Incorrect bitcoin address: %s" % (address))
            return
        if not is_float(amount_str):
            self.messages_view.error("Incorrect amount: %s" % (amount_str))
            return
        self.account.send_transaction(float(amount_str), address, 0)
        self.wallet_view.sender_view.close()
    
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
    wallet = Wallet(BSDDBWalletDatabase(bsddb_env, filename), runmode)
    balance = Mock({"get_confirmed" : 175877, "get_unconfirmed" : 2828727, "get_height" : 3}, accept_all_methods=True)
    def make_transaction(amount, to_adress, fee):
        print  amount, to_adress, fee
    wallet_manager = Mock(attributes={"wallet" : wallet, "balance" : balance, "make_transaction" : make_transaction}, )
    app = wx.App(False)
    frame = wx.Frame(None, size=(600,500))
    wallet_view = WalletPanel(frame)
    WalletPresenter(wallet_manager, wallet_view, MessageView(None))
    
    frame.Show()
    app.MainLoop()


