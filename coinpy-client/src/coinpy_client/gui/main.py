# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from coinpy.model.protocol.runmode import MAIN, TESTNET
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
import random
import wx
from coinpy_client.gui.view.mainwindow import MainWindow
from coinpy_client.gui.bitcoin_client import BitcoinClient

class CoinpyApp():
    def __init__(self, nodeparams, data_directory): 
        self.app = wx.App(False) #turn of graphical error console
        self.mainwindow = MainWindow(None, wx.ID_ANY, "Coinpy", size=(1000, 650))
        self.client = BitcoinClient(self.mainwindow.get_logger(), nodeparams, data_directory)

        self.mainwindow.subscribe(MainWindow.EVT_CMD_EXIT, self.on_command_exit)
        self.mainwindow.subscribe(MainWindow.EVT_CMD_OPEN_WALLET, self.on_command_open_wallet)
        self.client.subscribe(BitcoinClient.EVT_WALLET_OPENED, self.on_wallet_opened)
        
        self.mainwindow.node_view.connect_to(self.client.node)
        
    def on_command_exit(self, event):
        self.mainwindow.Destroy()
        self.client.stop()
        
    def on_command_open_wallet(self, event):
        wallet = self.client.open_wallet(event.file)
    
    def on_wallet_opened(self, event):
        self.mainwindow.add_wallet(event.filename, event.wallet)
        
    def run(self):
        self.mainwindow.Show()
        self.client.start()
        self.app.MainLoop()

if __name__ == '__main__':
        
    runmode = TESTNET
    
    
    nodeparams = NodeParams(runmode=runmode,
                            port=8080,
                            version=60000,
                            enabledservices=SERVICES_NODE_NETWORK,
                            nonce=random.randint(0, 2**64),
                            sub_version_num="/coinpy:0.0.1/")
    bitcoin = CoinpyApp(nodeparams, ((runmode == TESTNET) and "data_testnet" or "data_main"))
    bitcoin.run()
