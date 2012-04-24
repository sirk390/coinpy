# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
import wx.aui
from coinpy_client.view.wallet.wallet_notebook import WalletNotebook
from coinpy_client.view.log.logpanel import LogPanel
import logging
from coinpy_client.view.log.loghandler import GuiLogHandler
from coinpy.tools.observer import Observable
import os
from coinpy_client.view.node_view import NodeView
from coinpy_client.view.pools_panel import PoolsPanel
from coinpy_client.view.message_view import MessageView
from coinpy_client.view.blockchain.blockchain_summary_view import BlockchainSummaryView




class MainWindow(wx.Frame, Observable):
    EVT_CMD_OPEN_WALLET = Observable.createevent()
    EVT_CMD_NEW_WALLET = Observable.createevent()
    EVT_CMD_CLOSE_WALLET = Observable.createevent()
    EVT_CMD_CLOSE = Observable.createevent()
    
    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                            wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        Observable.__init__(self)
    
        # Create Menu
        mb = wx.MenuBar()

        # File
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_NEW, "New")
        self.Bind(wx.EVT_MENU, self.on_cmd_new_wallet, id=wx.ID_NEW)
        file_menu.Append(wx.ID_OPEN, "Open")
        self.Bind(wx.EVT_MENU, self.on_cmd_open_wallet, id=wx.ID_OPEN)
        file_menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit_menu, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        # Window
        ID_MENU_SHOWHIDE_CONNECTIONS = wx.NewId()
        ID_MENU_SHOWHIDE_LOGS = wx.NewId()
        ID_MENU_SHOWHIDE_POOLS = wx.NewId()
        ID_MENU_SHOWHIDE_BLOCKCHAIN_SUMMARY = wx.NewId()
        window_menu = wx.Menu()
        self.mi_showhide_connections = window_menu.Append(ID_MENU_SHOWHIDE_CONNECTIONS, "Connections", kind=wx.ITEM_CHECK)
        self.mi_showhide_connections.Check(True)
        self.mi_showhide_logs = window_menu.Append(ID_MENU_SHOWHIDE_LOGS, "Logs", kind=wx.ITEM_CHECK)
        self.mi_showhide_logs.Check(True)
        self.mi_showhide_pools = window_menu.Append(ID_MENU_SHOWHIDE_POOLS, "Pools", kind=wx.ITEM_CHECK)
        self.mi_showhide_pools.Check(False)
        self.mi_showhide_blockchain_summary = window_menu.Append(ID_MENU_SHOWHIDE_BLOCKCHAIN_SUMMARY, "Blockchain", kind=wx.ITEM_CHECK)
        self.mi_showhide_blockchain_summary.Check(True)
        mb.Append(file_menu, "File")
        mb.Append(window_menu, "Window")
        self.SetMenuBar(mb)
        self.Bind(wx.EVT_MENU, self.on_showhide_connections, id=ID_MENU_SHOWHIDE_CONNECTIONS)
        self.Bind(wx.EVT_MENU, self.on_showhide_logs, id=ID_MENU_SHOWHIDE_LOGS)
        self.Bind(wx.EVT_MENU, self.on_showhide_pools, id=ID_MENU_SHOWHIDE_POOLS)
        self.Bind(wx.EVT_MENU, self.on_showhide_blockchain_summary, id=ID_MENU_SHOWHIDE_BLOCKCHAIN_SUMMARY)

        
        # Create Child Windows
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        
        self.nb_wallet = WalletNotebook(self)
        self.log_panel = LogPanel(self)
        self.node_view = NodeView(self)
        self.pools_view = PoolsPanel(self, size=(250,300))
        self.blockchain_summary_view = BlockchainSummaryView(self, size=(10, 10))
        self._mgr.AddPane(self.nb_wallet, wx.aui.AuiPaneInfo().
                  Name("wallet_notebook").Caption("Wallet Notebook").MaximizeButton(True).
                  CenterPane())
        self._mgr.AddPane(self.pools_view, wx.aui.AuiPaneInfo().
                  Name("pools").Layer(2).Caption("Pools").MaximizeButton(True).
                  Right().Hide())
        self._mgr.AddPane(self.node_view, wx.aui.AuiPaneInfo().
                  Name("node").Layer(1).BestSize(wx.Size(300,500)).Caption("Connections").MaximizeButton(True).
                  Right())
        self._mgr.AddPane(self.log_panel, wx.aui.AuiPaneInfo().
                  Name("logs").Caption("Logs").MaximizeButton(True).
                  Bottom())
        blockchain_summary_paneinfo = wx.aui.AuiPaneInfo(). \
                  Name("blockchain_summary").BestSize(wx.Size(300,150)).Caption("Blockchain").Layer(1). \
                  Right().MaximizeButton(True)
        blockchain_summary_paneinfo.dock_proportion = 20000
        self._mgr.AddPane(self.blockchain_summary_view, blockchain_summary_paneinfo)
               
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.on_close_pane)
        self._mgr.Update()
        #Statusbar
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        #MessageBoxes
        self.messages_view = MessageView(self)
        
        self.nb_wallet.subscribe(self.nb_wallet.EVT_CLOSE_WALLET, self.on_cmd_close_wallet)
 
        
    def add_child_frame(self, childclass, title):
        child_frame = wx.aui.AuiMDIChildFrame(self, -1, title=title)
        child_inst = childclass()
        sizer = wx.BoxSizer()
        sizer.Add(child_inst, 1, wx.EXPAND)
        child_frame.SetSizer(sizer)
        
    def get_logger(self):
        logger = logging.getLogger(name="coinpy")
        logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        #Stdout
        #stdout = logging.StreamHandler(sys.stdout)
        handler = GuiLogHandler(self.log_panel)
        handler.setLevel(logging.INFO)
        #logger.addHandler(stdout)
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        return logger
    
    def on_cmd_new_wallet(self, event):
        dlg = wx.FileDialog(
            self, message="Select a wallet.dat filename",
            defaultDir=os.getcwd(), 
            defaultFile="wallet.dat",
            style=wx.SAVE | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fire(self.EVT_CMD_NEW_WALLET, file=dlg.GetPath())

    def on_cmd_open_wallet(self, event):
        dlg = wx.FileDialog(
            self, message="Select a wallet.dat file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard="wallet.dat (*.dat)|*.dat",
            style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.fire(self.EVT_CMD_OPEN_WALLET, file=dlg.GetPath())

    def on_cmd_close_wallet(self, event):
        self.fire(self.EVT_CMD_CLOSE_WALLET, id=event.id)
        
    def on_exit_menu(self, event):
        self.Close()   
        
    def on_close(self, event):
        #self.Destroy()
        self.fire(self.EVT_CMD_CLOSE)
    
    def on_close_pane(self, event):
        pane = event.GetPane()
        if pane.name == 'node':
            self.mi_showhide_connections.Check(False)
        if pane.name == 'logs':
            self.mi_showhide_logs.Check(False)
        if pane.name == 'pools':
            self.mi_showhide_pools.Check(False)
        if pane.name == 'blockchain_summary':
            self.mi_showhide_blockchain_summary.Check(False)
    
    def showhide_pane(self, pane_name, menuitem):
        pane = self._mgr.GetPane(pane_name)
        isvisible = pane.IsShown()
        if (isvisible):
            pane.Hide()
            menuitem.Check(False)
        else:
            pane.Show()
            menuitem.Check(True)
        self._mgr.Update()
        
    def on_showhide_connections(self, event):
        self.showhide_pane("node", self.mi_showhide_connections)
        
    def on_showhide_pools(self, event):
        self.showhide_pane("pools", self.mi_showhide_pools)

    def on_showhide_logs(self, event):
        self.showhide_pane("logs", self.mi_showhide_logs)

    def on_showhide_blockchain_summary(self, event):
        self.showhide_pane("blockchain_summary", self.mi_showhide_blockchain_summary)
    
 
        
#self.app = wx.App(False) #turn of graphical error console
        
if __name__ == '__main__':
    app = wx.App(False)
    mainwindow = MainWindow(None, None, size=(1000,400))
    mainwindow.Show()
    app.MainLoop()
       