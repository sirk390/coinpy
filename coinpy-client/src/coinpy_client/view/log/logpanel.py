# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
import wx
import wx.richtext
             
class LogPanel(wx.Panel):
    def __init__(self, parent):
        super(LogPanel, self).__init__(parent, size=wx.Size(150, 300))
        self.richtext = wx.richtext.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL, size=wx.Size(50, 20))
        
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        #self.sizer.Add(wx.StaticText(self, -1, "Logs: "), 0, wx.EXPAND)
        self.sizer.Add(self.richtext, 1, wx.EXPAND)
        self.SetSizer(self.sizer)