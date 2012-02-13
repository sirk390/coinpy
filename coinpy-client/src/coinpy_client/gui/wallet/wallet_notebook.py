# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
import wx
import wx.aui

class WalletNotebook(wx.aui.AuiNotebook):
    def __init__(self, parent):
        super(WalletNotebook, self).__init__(parent, -1,  wx.DefaultPosition, wx.Size(400, 300))
        
        page = wx.TextCtrl(self, -1, "wallet.dat 1",
                               style=wx.TE_MULTILINE|wx.TE_RICH|wx.VSCROLL)
        self.AddPage(page, "wallet.dat 1")
            
    def add_wallet(self, wallet):
        pass
    