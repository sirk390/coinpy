# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
import wx
import wx.aui
from coinpy_client.gui.view.wallet.wallet import Wallet
import wx.lib.scrolledpanel

class WalletNoteBookPage(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent):
        super(WalletNoteBookPage, self).__init__(parent)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.wallet = Wallet(self)
        self.sizer.Add(self.wallet, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetupScrolling()
    
class WalletNotebook(wx.aui.AuiNotebook):
    def __init__(self, parent):
        super(WalletNotebook, self).__init__(parent, -1,  wx.DefaultPosition, wx.Size(400, 300))
        
        page = WalletNoteBookPage(self)
        self.AddPage(page, "wallet.dat 1")
            
    def add_wallet(self, wallet):
        pass
