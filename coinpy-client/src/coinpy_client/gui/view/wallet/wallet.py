# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx
from coinpy_client.gui.view.wallet.balance import BalancePanel
from coinpy_client.gui.view.wallet.keys_panel import KeysPanel
from coinpy_client.gui.view.wallet.address_book_panel import AddressBookPanel
from coinpy_client.gui.view.wallet.transations_panel import TransactionsPanel

class Wallet(wx.Panel):
    def __init__(self, parent):
        super(Wallet, self).__init__(parent, style=wx.SIMPLE_BORDER)
        
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.balance = BalancePanel(self)
        self.keys = KeysPanel(self)
        self.address_book = AddressBookPanel(self)
        self.transactions = TransactionsPanel(self)
        self.sizer.Add(self.balance, 0, wx.EXPAND)
        self.sizer.Add(self.keys, 0, wx.EXPAND)
        self.sizer.Add(self.address_book, 0, wx.EXPAND)
        self.sizer.Add(self.transactions, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    wallet = Wallet(frame)
    frame.Show()
    app.MainLoop()
