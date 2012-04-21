# -*- coding:utf-8 -*-
"""
Created on 29 Feb 2012

@author: kris
"""
import wx
from coinpy.tools.observer import Observable
from coinpy_client.view.guithread import guithread

class EnterPassphraseView(wx.Dialog, Observable):
    EVT_ENTERED_PASSPHRASE = Observable.createevent()
    def __init__(self, reactor, parent, size=(250, 150)):
        wx.Dialog.__init__(self, parent, size=size, title="Enter Passphrase", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        Observable.__init__(self,reactor)

        # Create Controls
        self.passphrase_label = wx.StaticText(self, -1, "Passphrase:")
        self.passphrase_textctrl = wx.TextCtrl(self, -1, "", size=(250,-1), style=wx.TE_PASSWORD)
        
        self.hide_characters_label = wx.StaticText(self, -1, "Hide characters:")
        self.hide_characters_checkbox = wx.CheckBox(self, -1)
        self.hide_characters_checkbox.SetValue(True)
        
        # Setup Sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.formsizer = wx.FlexGridSizer(2, 2)
        self.formsizer.Add(self.passphrase_label, 0, wx.LEFT|wx.ALL, 5)
        self.formsizer.Add(self.passphrase_textctrl, 1, wx.LEFT|wx.ALL|wx.EXPAND, 5)
        self.formsizer.Add(self.hide_characters_label, 0, wx.LEFT|wx.ALL, 5)
        self.formsizer.Add(self.hide_characters_checkbox, 1, wx.LEFT|wx.ALL, 5)
        
        self.formsizer.AddGrowableCol(1)

        sizer.Add(self.formsizer, 1, wx.EXPAND|wx.TOP, 20)
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
        self.hide_characters_checkbox.Bind(wx.EVT_CHECKBOX, self.on_hide_characters_checkbox)
        
    def on_hide_characters_checkbox(self, event):
        hide_characters = self.hide_characters_checkbox.GetValue()
        style = wx.TE_PASSWORD if hide_characters else 0
        value = self.passphrase_textctrl.GetValue()
        new_passphrase_textctrl = wx.PreTextCtrl()
        #create hidden to prevent visible repositionning
        new_passphrase_textctrl.Show(False)
        new_passphrase_textctrl.Create(self, -1, "", size=(250,-1), style=style)
        new_passphrase_textctrl.SetValue(value)
        self.formsizer.Replace(self.passphrase_textctrl, new_passphrase_textctrl)
        self.passphrase_textctrl.Destroy()
        self.passphrase_textctrl = new_passphrase_textctrl
        new_passphrase_textctrl.Show(True)
        self.formsizer.Layout()
        
    @guithread  
    def open(self):
        self.Show(True)

    def on_ok(self, event):
        self.Show(False)
        self.fire(self.EVT_ENTERED_PASSPHRASE)
        
    def on_cancel(self):
        self.Show(False)
               
    def get_passphrase(self):
        return self.passphrase_textctrl.GetValue()
        
    def set_passphrase(self, passphrase):
        return self.passphrase_textctrl.SetValue(passphrase)
            
    
if __name__ == '__main__':
    from coinpy.tools.reactor.reactor import Reactor
    app = wx.App(False)
    s = EnterPassphraseView(None, None)
    def on_entered(event):
        print "OK", s.get_passphrase()
        s.close()
    s.subscribe(s.EVT_ENTERED_PASSPHRASE, on_entered)
    s.open()
    app.MainLoop()

