import wx

class ProgressView(wx.Dialog):
    def __init__(self, parent, title, message, size=(200, 200)):
        self.parent = parent
        self.title = title
        self.message = message
        self.max = 100
        
    def open(self):
        self.dlg = wx.ProgressDialog(self.title, self.message,
                                     maximum = self.max, parent=self.parent,
                                     style = wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME)
        #more styles: wx.PD_CAN_ABORT, wx.PD_ESTIMATED_TIME, wx.PD_REMAINING_TIME

    def set_progress(self, value):
        self.dlg.Update(value)

    def close(self):
        self.dlg.Destroy()
    
    
if __name__ == '__main__':
    from coinpy.tools.reactor.reactor import reactor
    from coinpy.tools.reactor.wx_plugin import WxPlugin
    
    reactor.install(WxPlugin())
    r = ProgressView(None,"Opening", "Processing")
    r.open()
    p = 0
    def update_progress():
        global p
        r.set_progress(p)
        p += 5
        if p < 100:
            reactor.call_later(0.01, update_progress)
        else:
            reactor.stop()
    update_progress()
    reactor.run()
    