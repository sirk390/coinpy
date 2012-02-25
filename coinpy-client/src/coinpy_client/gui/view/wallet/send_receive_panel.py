# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx

class SendReceivePanel(wx.Panel):
    def __init__(self, parent):
        super(SendReceivePanel, self).__init__(parent)#, style=wx.SIMPLE_BORDER for debug
        
        self.send = wx.Button(self, label="Send")
        self.receive = wx.Button(self, label="Receive")
        
        self.sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.sizer.Add(self.send, 0, wx.LEFT)
        self.sizer.Add(self.receive, 0, wx.LEFT)
        self.SetSizer(self.sizer)
        