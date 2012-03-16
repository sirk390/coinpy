# -*- coding:utf-8 -*-
"""
Created on 11 Mar 2012

@author: kris
"""
import wx

class BlockchainSummaryView(wx.Panel):
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size=size)
        txtctrl_style = wx.TE_READONLY|wx.BORDER_NONE|wx.TE_RIGHT
        txtctrl_color = (196,196,196)
        self.block_label = wx.StaticText(self, -1, "Block Height:")
        self.height_textctrl = wx.TextCtrl(self, -1, "", size=(80,-1), style=txtctrl_style)
        self.height_textctrl.SetBackgroundColour(txtctrl_color)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.block_label)
        self.sizer.Add(self.height_textctrl)
        
        self.sizer_border = wx.BoxSizer(wx.VERTICAL)
        self.sizer_border.Add(self.sizer, 0, wx.ALL, 5)
        self.SetSizer(self.sizer_border)
        
    def set_height(self, str):
        self.height_textctrl.SetValue(str)
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, size=(500, 600))
    view = BlockchainSummaryView(frame)
    view.set_height("8789")

    frame.Show()
    app.MainLoop()