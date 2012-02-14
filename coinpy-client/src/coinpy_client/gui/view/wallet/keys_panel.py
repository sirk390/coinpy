# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx

class KeysPanel(wx.Panel):
    def __init__(self, parent):
        super(KeysPanel, self).__init__(parent, style=wx.SIMPLE_BORDER)
        
        self.list = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.list.InsertColumn(0, "Public Key")
        self.list.InsertColumn(1, "Private Key")
        self.list.InsertColumn(3, "Pool")
        self.list.InsertColumn(4, "Pool Time")
        self.list.InsertColumn(1, "Address")
        self.list.InsertColumn(1, "Name")
        
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(wx.StaticText(self, -1, "Keys: "))
        self.sizer.Add(self.list, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        