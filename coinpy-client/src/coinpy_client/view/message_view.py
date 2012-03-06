# -*- coding:utf-8 -*-
"""
Created on 1 Mar 2012

@author: kris
"""
import wx

class MessageView():
    def __init__(self, parent):
        self.parent = parent
   
    def info(self, message, title=""): 
        dlg = wx.MessageDialog(self.parent, message, title, wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
    def error(self, message, title=""): 
        dlg = wx.MessageDialog(self.parent, message, title, wx.OK|wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
