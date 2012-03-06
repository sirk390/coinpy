# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
import wx
import wx.aui
from coinpy_client.gui.view.wallet.wallet_panel import WalletPanel
import wx.lib.scrolledpanel
import os

class WalletNoteBookPage(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent):
        super(WalletNoteBookPage, self).__init__(parent)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.wallet_panel = WalletPanel(self)
        self.sizer.Add(self.wallet_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetupScrolling()
    
class WalletNotebook(wx.aui.AuiNotebook):
    def __init__(self, parent):
        super(WalletNotebook, self).__init__(parent, -1,  wx.DefaultPosition, wx.Size(400, 300))
        
        #page = WalletNoteBookPage(self)
        #self.AddPage(page, "wallet.dat 1")

    def add_wallet_view(self, label):
        page = WalletNoteBookPage(self)
        self.AddPage(page, label)
        return page.wallet_panel

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    notebook = WalletNotebook(frame)
    page = WalletNoteBookPage(notebook)
    notebook.AddPage(page, "wallet1")
    frame.Show()
    app.MainLoop()
