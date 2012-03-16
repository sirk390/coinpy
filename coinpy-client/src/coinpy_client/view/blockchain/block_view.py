# -*- coding:utf-8 -*-
"""
Created on 9 Mar 2012

@author: kris
"""
import wx
 
class BlockView(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent)
        #Block
        txtctrl_style = wx.TE_READONLY|wx.BORDER_SIMPLE #|wx.TE_RIGHT
        txtctrl_color = (196,196,196)
        font_large = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        font_mono = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.block_label = wx.StaticText(self, -1, "Block", size=(350,30))
        self.block_label.SetFont(font_large)
        self.hash_label = wx.StaticText(self, -1, "Hash:")
        self.hash_textctrl = wx.TextCtrl(self, -1, "", size=(390,-1), style=txtctrl_style)
        self.hash_textctrl.SetBackgroundColour(txtctrl_color)
        self.hash_textctrl.SetFont(font_mono)
        self.previous_block_label = wx.StaticText(self, -1, "Previous block:")
        self.previous_block_textctrl = wx.TextCtrl(self, -1, "", size=(390,-1), style=txtctrl_style)
        self.previous_block_textctrl.SetBackgroundColour(txtctrl_color)
        self.previous_block_textctrl.SetFont(font_mono)
        self.next_block_label = wx.StaticText(self, -1, "Next block:")
        self.next_block_textctrl = wx.TextCtrl(self, -1, "", size=(390,-1), style=txtctrl_style)
        self.next_block_textctrl.SetBackgroundColour(txtctrl_color)
        self.next_block_textctrl.SetFont(font_mono)
        self.time_label = wx.StaticText(self, -1, "Time:")
        self.time_textctrl = wx.TextCtrl(self, -1, "", size=(150,-1), style=txtctrl_style)
        self.time_textctrl.SetBackgroundColour(txtctrl_color)
        self.time_textctrl.SetFont(font_mono)
        self.difficulty_label = wx.StaticText(self, -1, "Difficulty:")
        self.difficulty_textctrl = wx.TextCtrl(self, -1, "", size=(150,-1), style=txtctrl_style)
        self.difficulty_textctrl.SetBackgroundColour(txtctrl_color)
        self.difficulty_textctrl.SetFont(font_mono)
        self.merkle_label = wx.StaticText(self, -1, "Merkle root:")
        self.merkle_textctrl = wx.TextCtrl(self, -1, "", size=(390,-1), style=txtctrl_style)
        self.merkle_textctrl.SetBackgroundColour(txtctrl_color)
        self.merkle_textctrl.SetFont(font_mono)
        self.nonce_label = wx.StaticText(self, -1, "Nonce:")
        self.nonce_textctrl = wx.TextCtrl(self, -1, "", size=(150,-1), style=txtctrl_style)
        self.nonce_textctrl.SetBackgroundColour(txtctrl_color)
        self.nonce_textctrl.SetFont(font_mono)
        #Transactions
        self.transactions_label = wx.StaticText(self, -1, "Transactions", size=(350,-1))
        self.transactions_label.SetFont(font_large)
        
        self.transactions_listctrl = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        
        self.transactions_listctrl.InsertColumn(0, "Transaction")
        self.transactions_listctrl.InsertColumn(1, "Amount")
        self.transactions_listctrl.InsertColumn(2, "Fee")
        self.transactions_listctrl.InsertColumn(3, "Type")
      
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        formsizer = wx.FlexGridSizer(7, 2, vgap=2)
        formsizer.Add(self.hash_label, 0)
        formsizer.Add(self.hash_textctrl,  0, wx.EXPAND)
        formsizer.Add(self.previous_block_label, 0)
        formsizer.Add(self.previous_block_textctrl, 0, wx.EXPAND)
        formsizer.Add(self.next_block_label)
        formsizer.Add(self.next_block_textctrl, 0,wx.EXPAND)
        formsizer.Add(self.time_label, 0)
        formsizer.Add(self.time_textctrl, 0)
        formsizer.Add(self.difficulty_label, 0)
        formsizer.Add(self.difficulty_textctrl, 0)
        formsizer.Add(self.merkle_label, 0)
        formsizer.Add(self.merkle_textctrl, 0, wx.EXPAND)
        formsizer.Add(self.nonce_label, 0)
        formsizer.Add(self.nonce_textctrl, 0)
        formsizer.AddGrowableCol(1)
        
        """
        tx_table = wx.FlexGridSizer(20, 5, vgap=2)
        tx_table.Add(self.thlabel_txtable)
        tx_table.Add(self.thlabel_amount)
        tx_table.Add(self.thlabel_fee)
        tx_table.Add(self.thlabel_from)
        tx_table.Add(self.thlabel_to)
        tx_table.AddGrowableCol(0)
        tx_table.AddGrowableCol(1)
        tx_table.AddGrowableCol(2)
        tx_table.AddGrowableCol(3)
        tx_table.AddGrowableCol(4)"""
        
        self.sizer.Add(self.block_label)
         
        self.sizer.Add(formsizer, 0, wx.EXPAND)
        self.sizer.Add(self.transactions_label)
        self.sizer.Add(self.transactions_listctrl, 1, wx.EXPAND)
        
        
        self.bestsize = (600,25)
        self.SetSize(self.GetBestSize())
        self.SetSizer(self.sizer)
    
    def set_hash(self, str):
        self.hash_textctrl.SetValue(str)

    def set_previous_block(self, str):
        self.previous_block_textctrl.SetValue(str)

    def set_next_block(self, str):
        self.next_block_textctrl.SetValue(str)

    def set_time(self, str):
        self.time_textctrl.SetValue(str)

    def set_difficulty(self, str):
        self.difficulty_textctrl.SetValue(str)

    def set_merkle(self, str):
        self.merkle_textctrl.SetValue(str)

    def set_nonce(self, str):
        self.nonce_textctrl.SetValue(str)

       
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, size=(500, 600))
    BlockView(frame)


    frame.Show()
    app.MainLoop()