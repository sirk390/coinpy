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

if __name__ == '__main__':
    app = wx.App(False)
    messages = MessageView(None)
    messages.info("hello", "title")
    messages.error("error", "title")
