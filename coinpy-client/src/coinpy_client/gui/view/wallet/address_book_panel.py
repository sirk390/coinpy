# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx

class AddressBookPanel(wx.Panel):
    def __init__(self, parent):
        super(AddressBookPanel, self).__init__(parent, style=wx.SIMPLE_BORDER)
        
        self.list = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.list.InsertColumn(0, "Name")
        self.list.InsertColumn(1, "Address")
        
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(wx.StaticText(self, -1, "Addresses: "))
        self.sizer.Add(self.list, 0, wx.EXPAND)
        self.SetSizer(self.sizer)
        