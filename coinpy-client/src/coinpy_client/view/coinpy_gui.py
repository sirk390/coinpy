# -*- coding:utf-8 -*-
"""
Created on 21 Feb 2012

@author: kris
"""
from coinpy_client.view.mainwindow import MainWindow
import wx
import threading
from coinpy.tools.observer import Observable
from coinpy_client.view.message_view import MessageView

class CoinpyGUI(Observable):
    EVT_CMD_CLOSE = Observable.createevent()
   
    def __init__(self):
        super(CoinpyGUI, self).__init__()
        self.app = wx.App(False)
        self.mainwindow = MainWindow(None, wx.ID_ANY, "Coinpy", size=(1000, 650))
        self.mainwindow.subscribe(MainWindow.EVT_CMD_CLOSE, self.on_exit)
        self.messages_view = MessageView(self.mainwindow)
        
    def on_exit(self, event):
        self.fire(self.EVT_CMD_CLOSE)
        
    def get_logger(self):   
        return (self.mainwindow.get_logger())
        
    def mainloop(self):   
        self.mainwindow.Show()
        self.app.MainLoop()
        
    def stop(self):   
        self.mainwindow.Destroy()
        
if __name__ == '__main__':
    def on_exit(event):
        print "exited"
    mainview = CoinpyGUI()
    mainview.mainloop()
    