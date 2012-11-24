import wx
from coinpy.tools.observer import Observable
from coinpy_client.view.guithread import guithread

class SendView(wx.Dialog, Observable):
    EVT_SELECT_VALUE= Observable.createevent()
    def __init__(self, parent, size=(300, 200)):
        wx.Dialog.__init__(self, parent, size=size, title="Send", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
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
        
    @guithread  
    def open(self):
        self.Show(True)

    def on_ok(self, event):
        self.fire(self.EVT_SELECT_VALUE)

    def on_cancel(self):
        self.Show(False)
               
    def address(self):
        return self.address_textctrl.GetValue()
        
    def amount(self):
        return self.amount_textctrl.GetValue()
    
    @guithread  
    def close(self):
        self.Show(False)
    
if __name__ == '__main__':
    from coinpy.tools.reactor.reactor import Reactor
    app = wx.App(False)
    s = SendView(None)
    def validate(event):
        print "validating..."
        s.close()
    s.subscribe(s.EVT_SELECT_VALUE, validate)
    s.open()
    app.MainLoop()

