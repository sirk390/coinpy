# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx

class BalancePanel(wx.Panel):
    def __init__(self, parent):
        super(BalancePanel, self).__init__(parent, style=wx.SIMPLE_BORDER)
        
        
        self.sizer = wx.GridBagSizer(3, 2)
        
        self.sizer.Add( wx.StaticText(self, -1, "Balance: "), (0,0))
        self.sizer.Add( wx.StaticText(self, -1, "0.0 BTC "), (0,1))
        self.sizer.Add( wx.StaticText(self, -1, "Unconfirmed: "), (1,0))
        self.sizer.Add( wx.StaticText(self, -1, "0.0 BTC "), (1,1))
        self.sizer.Add( wx.StaticText(self, -1, "Block height: "), (2,0))
        self.sizer.Add( wx.StaticText(self, -1, "0"), (2,1))
        self.SetSizerAndFit(self.sizer)
        