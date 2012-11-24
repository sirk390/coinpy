import wx

class WxPlugin(object):
    def __init__(self):
        self.app = wx.App(False) 
        self.evtloop = wx.EventLoop() 
        wx.EventLoop.SetActive(self.evtloop) 
        
    def install(self, reactor):
        pass
        
    def run(self):
        #wx.Yield()
        donework = False
        while self.evtloop.Pending():
            self.evtloop.Dispatch()
            donework = True
        self.app.ProcessIdle()
        return False
   