# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
import wx
import wx.aui
from coinpy_client.view.wallet.wallet_panel import WalletPanel
import wx.lib.scrolledpanel
import os
from coinpy.tools.observer import Observable

class WalletNoteBookPage(wx.Panel): #.lib.scrolledpanel.ScrolledPanel
    def __init__(self, parent):
        super(WalletNoteBookPage, self).__init__(parent)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.wallet_panel = WalletPanel(self)
        self.sizer.Add(self.wallet_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        #self.SetupScrolling()
    
class WalletNotebook(wx.aui.AuiNotebook, Observable):
    EVT_CLOSE_WALLET = Observable.createevent()
    def __init__(self, parent):
        Observable.__init__(self)
        wx.aui.AuiNotebook.__init__(self, parent, -1,  wx.DefaultPosition, wx.Size(400, 300))
        
        #page = WalletNoteBookPage(self)
        #self.AddPage(page, "wallet.dat 1")
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_wallet_close)
        self.pages = {} # id => WalletNoteBookPage
       
    def add_wallet_view(self, id, label):
        page = WalletNoteBookPage(self)
        self.pages[id] = page
        self.AddPage(page, label)
        index = self.GetPageIndex(page)
        self.SetPageText(index, label + "%d" % index)
        return page.wallet_panel
    
    def find_page_index(self, page_id):
        for id, page in self.pages.iteritems():
            if id == page_id:
                return self.GetPageIndex(page)
        return None
    
    def find_page_id(self, index):
        for id, page in self.pages.iteritems():
            if self.GetPageIndex(page)== index:
                return id
        return None
      
    def remove_wallet_view(self, id):
        index = self.find_page_index(id)
        self.pages[id].Destroy()
        del self.pages[id]
        return self.RemovePage(index)

    def on_wallet_close(self, event):
        event.Veto()
        self.fire(self.EVT_CLOSE_WALLET, id=self.find_page_id(event.Int))
   

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    notebook = WalletNotebook(frame)
    notebook.add_wallet_view(2, "wallet1")
    notebook.add_wallet_view(4, "wallet2")
    notebook.remove_wallet_view(4)
    notebook.remove_wallet_view(2)
    #for w in notebook.GetChildren():
    #    print w.GetName(), type(w)
    frame.Show()
    app.MainLoop()
