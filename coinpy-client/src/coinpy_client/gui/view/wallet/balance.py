# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx
from coinpy.model.constants.bitcoin import COIN

class BalancePanel(wx.Panel):
    def __init__(self, parent):
        super(BalancePanel, self).__init__(parent)
       
        self.confirmed_count_label = wx.StaticText(self, -1, "")
        self.unconfirmed_count_label = wx.StaticText(self, -1, "")
        self.block_height_label = wx.StaticText(self, -1, "")
        
        self.sizer = wx.GridBagSizer(3, 2)
        self.sizer.Add( wx.StaticText(self, -1, "Balance: "), (0,0))
        self.sizer.Add( self.confirmed_count_label, (0,1))
        self.sizer.Add( wx.StaticText(self, -1, "Unconfirmed: "), (1,0))
        self.sizer.Add( self.unconfirmed_count_label, (1,1))
        self.sizer.Add( wx.StaticText(self, -1, "Block height: "), (2,0))
        self.sizer.Add( self.block_height_label, (2,1))
        self.SetSizerAndFit(self.sizer)
        
    def set_balance(self, confirmed, unconfirmed, height):
        self.confirmed_count_label.SetLabel("%f BTC" % (confirmed * 1.0 / COIN))
        self.unconfirmed_count_label.SetLabel("%f BTC" % (unconfirmed * 1.0 / COIN))
        self.block_height_label.SetLabel("%d" % (height))
        
