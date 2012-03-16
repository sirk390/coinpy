# -*- coding:utf-8 -*-
"""
Created on 9 Mar 2012

@author: kris
"""
import wx
 
class TransactionView(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent)
        

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, size=(500, 600))
    TransactionView(frame)


    frame.Show()
    app.MainLoop()