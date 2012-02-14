# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx

class TransactionsPanel(wx.Panel):
    def __init__(self, parent):
        super(TransactionsPanel, self).__init__(parent, style=wx.SIMPLE_BORDER)
        
        self.list = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.list.InsertColumn(0, "Date")
        self.list.InsertColumn(1, "Address")
        self.list.InsertColumn(3, "Amount")
        
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(wx.StaticText(self, -1, "Transactions: "))
        self.sizer.Add(self.list, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        