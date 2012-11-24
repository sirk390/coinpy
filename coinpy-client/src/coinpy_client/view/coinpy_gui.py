from coinpy_client.view.mainwindow import MainWindow
import wx
from coinpy.tools.observer import Observable
from coinpy_client.view.message_view import MessageView
from coinpy.tools.reactor.reactor import reactor
from coinpy.tools.reactor.wx_plugin import WxPlugin

reactor.install(WxPlugin())
    
class CoinpyGUI(Observable):
    EVT_CMD_CLOSE = Observable.createevent()
   
    def __init__(self):
        super(CoinpyGUI, self).__init__()
        self.mainwindow = MainWindow(None, wx.ID_ANY, "Coinpy", size=(1000, 650))
        self.mainwindow.subscribe(MainWindow.EVT_CMD_CLOSE, self.on_exit)
        self.messages_view = MessageView(self.mainwindow)
        
    def on_exit(self, event):
        self.fire(self.EVT_CMD_CLOSE)
        
    def get_logger(self):   
        return (self.mainwindow.get_logger())
        
    def start(self):   
        self.mainwindow.Show()
        
    def mainloop(self):   
        pass
    
    def stop(self):   
        self.mainwindow.Destroy()
        
if __name__ == '__main__':
    def on_exit(event):
        print "exited"
    mainview = CoinpyGUI()
    mainview.mainloop()
    