# -*- coding:utf-8 -*-
"""
Created on 29 Feb 2012

@author: kris
"""
import wx
from coinpy.tools.observer import Observable
from coinpy_client.view.guithread import guithread

class ReceiveView(wx.Dialog, Observable):
    EVT_SET_LABEL= Observable.createevent()
    
    def __init__(self, reactor, parent, size=(300, 200)):
        wx.Dialog.__init__(self, parent, size=size, title="Receive")
        Observable.__init__(self,reactor)

        # Create Controls
        self.address_label = wx.StaticText(self, -1, "Address:")
        self.address_textctrl = wx.TextCtrl(self, -1, "", size=(250,-1), style=wx.TE_READONLY|wx.BORDER_SIMPLE)
        self.address_textctrl.SetBackgroundColour((196,196,196))
        self.label_label = wx.StaticText(self, -1, "Label:")
        self.label_textctrl = wx.TextCtrl(self, -1, "", size=(80,-1))

        # Setup Sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        formsizer = wx.FlexGridSizer(2, 2)
        formsizer.Add(self.address_label, 0, wx.LEFT|wx.ALL, 5)
        formsizer.Add(self.address_textctrl, 1, wx.LEFT|wx.ALL|wx.EXPAND, 5)
        formsizer.Add(self.label_label, 0, wx.LEFT|wx.ALL, 5)
        formsizer.Add(self.label_textctrl, 1, wx.LEFT|wx.ALL|wx.EXPAND, 5)
        formsizer.AddGrowableCol(1)
    
        sizer.Add(formsizer, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 20)
        btnsizer = wx.StdDialogButtonSizer()
        ok_button = wx.Button(self, wx.ID_OK)
        ok_button.SetDefault()
        btnsizer.AddButton(ok_button)

        cancel_button = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(cancel_button)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        self.SetSizer(sizer)
        
        # Bind Events
        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        
    @guithread  
    def open(self):
        self.Show(True)

    def on_ok(self, event):
        self.Show(False)
        self.fire(self.EVT_SET_LABEL)

    def on_cancel(self):
        self.Show(False)
               
    def set_receive_address(self, address):
        self.address_textctrl.SetValue(address)
    
    def get_receive_address(self):
        return self.address_textctrl.GetValue()
    
    def get_label(self):
        return self.label_textctrl.GetValue()
    
    
if __name__ == '__main__':
    from coinpy.tools.reactor.reactor import Reactor
    app = wx.App(False)
    r = ReceiveView(None, None)
    r.set_receive_address("mhFwRrjRNt8hYeWtm9LwqCpCgXjF38RJqn")
    r.open()
    app.MainLoop()

