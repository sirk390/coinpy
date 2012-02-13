# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
import wx
import wx.richtext
             
class LogPanel(wx.richtext.RichTextCtrl):
    def __init__(self, parent):
        super(LogPanel, self).__init__(parent, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER, size=wx.Size(150, 300))
    