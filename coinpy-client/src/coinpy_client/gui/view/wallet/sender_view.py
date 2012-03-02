# -*- coding:utf-8 -*-
"""
Created on 29 Feb 2012

@author: kris
"""
import wx
from coinpy.tools.observer import Observable

class SendDialog(wx.Dialog, Observable):
    EVT_OK = Observable.createevent()
    EVT_CANCEL = Observable.createevent()
    def __init__(self, parent, size):
        wx.Dialog.__init__(self, parent, size=size, title="Send")
        Observable.__init__(self)
        # Create Controls
        self.address_label = wx.StaticText(self, -1, "To:")
        self.address_textctrl = wx.TextCtrl(self, -1, "", size=(250,-1))
        self.amount_label = wx.StaticText(self, -1, "Amount:")
        self.amount_textctrl = wx.TextCtrl(self, -1, "", size=(80,-1))
        # Setup Sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        formsizer = wx.FlexGridSizer(2, 2)
        formsizer.Add(self.address_label, 0, wx.LEFT|wx.ALL, 5)
        formsizer.Add(self.address_textctrl, 1, wx.LEFT|wx.ALL|wx.EXPAND, 5)
        formsizer.Add(self.amount_label, 0, wx.LEFT|wx.ALL, 5)
        formsizer.Add(self.amount_textctrl, 0, wx.LEFT|wx.ALL, 5)
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
        
    def on_ok(self, event):
        self.fire(self.EVT_OK)
        
    def address(self):
        return self.address_textctrl.GetValue()
    
    def amount(self):
        return self.amount_textctrl.GetValue()

class SenderView(Observable):
    EVT_SELECT_VALUE= Observable.createevent()
    def __init__(self, parent):
        super(SenderView, self).__init__()
        self.dlg = SendDialog(parent, size=(300, 200))
        self.dlg.CenterOnScreen()
        self.dlg.subscribe(self.dlg.EVT_CANCEL, self.on_cancel)
        self.dlg.subscribe(self.dlg.EVT_OK, self.on_ok)
        
    def open(self):
        self.dlg.ShowModal()

    def on_ok(self, event):
        self.fire(self.EVT_SELECT_VALUE)

    def on_cancel(self):
        self.dlg.EndModal(wx.ID_CANCEL)
                             
    def address(self):
        return self.dlg.address()
        
    def amount(self):
        return self.dlg.amount()
    
    def close(self):
        self.dlg.EndModal(wx.ID_OK)
    
if __name__ == '__main__':
    app = wx.App(False)
    s = SenderView()
    def validate(event):
        print "validating..."
        s.close()
    s.subscribe(s.EVT_OK, validate)
    s.open()
    
