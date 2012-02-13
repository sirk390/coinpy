# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
import wx
import wx.aui
from coinpy_client.gui.wallet.wallet_notebook import WalletNotebook
from coinpy_client.gui.log.logpanel import LogPanel
import logging
from coinpy_client.gui.log.loghandler import GuiLogHandler
from coinpy.tools.observer import Observable
import os

class MainWindow(wx.Frame, Observable):
    EVT_OPEN_WALLET = Observable.createevent()
    EVT_EXIT_COMMAND = Observable.createevent()
    
    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                            wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        Observable.__init__(self)
    
        # create menus
        mb = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, "Open")
        self.Bind(wx.EVT_MENU, self.on_open_wallet, id=wx.ID_OPEN)
        file_menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        window_menu = wx.Menu()
        mb.Append(file_menu, "File")
        mb.Append(window_menu, "Window")
        
        self.SetMenuBar(mb)

        
        # create child windows
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        
        self.nb_wallet = WalletNotebook(self)
        self.log_panel = LogPanel(self)
        self._mgr.AddPane(self.nb_wallet, wx.aui.AuiPaneInfo().
                  Name("wallet_notebook").Caption("Wallet Notebook").
                  CenterPane())
        self._mgr.AddPane(self.log_panel, wx.aui.AuiPaneInfo().
                  Name("logs").Caption("Logs").
                  CenterPane().Bottom())
        self._mgr.Update()
        # create statusbar
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
    
    def get_logger(self):
        logger = logging.getLogger(name="coinpy")
        logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        #Stdout
        #stdout = logging.StreamHandler(sys.stdout)
        handle = GuiLogHandler(self.log_panel)
        #logger.addHandler(stdout)
        handle.setFormatter(fmt)
        logger.addHandler(handle)
        return logger
    
    def on_open_wallet(self, event):
        dlg = wx.FileDialog(
            self, message="Select a wallet.dat file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard="wallet.dat (*.dat)|*.dat|",
            style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fire(self.EVT_OPEN_WALLET, file=dlg.GetPaths())
           
    def on_exit(self, event):
        self.Close()   
        
    def on_close(self, event):
        self.fire(self.EVT_EXIT_COMMAND)
        
        