# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from coinpy.tools.reactor.reactor import Reactor
from coinpy.lib.database.bsddb_env import BSDDBEnv
from coinpy.model.genesis import GENESIS
from coinpy.lib.database.blockchain.db_blockchain import BSDDbBlockChainDatabase
from coinpy.lib.bitcoin.blockchain.blockchain import Blockchain
from coinpy.lib.bitcoin.blockchain_with_pools import BlockchainWithPools
from coinpy.lib.bitcoin.wallet.wallet import Wallet
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
import threading
import os
from coinpy.tools.observer import Observable
from coinpy.node.network.sockaddr import SockAddr
from coinpy.node.network.bitcoin_port import BITCOIN_PORT
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.lib.bitcoin.wallet.wallet_balance import WalletBalance
import wx
from coinpy_client.view.coinpy_gui import CoinpyGUI
from coinpy_client.presenter.mainwindow_presenter import MainWindowPresenter
from coinpy_client.view.message_view import MessageView

class CoinpyPresenter():
    def __init__(self, service, view): 
        self.service = service
        self.view = view
        self.view.subscribe(self.view.EVT_CMD_CLOSE, self.on_command_close)
        self.mainwindow_presenter = MainWindowPresenter(self.service, view.mainwindow)
      
    def on_command_close(self, event):
        self.service.stop(self.on_service_exited)
        
    def on_service_exited(self):
        self.view.stop()

    def run(self):
        self.service.start()
        self.view.mainloop()
        #self.service.run()
       
if __name__ == '__main__':
    from coinpy.model.protocol.runmode import MAIN, TESTNET
    from coinpy.node.config.nodeparams import NodeParams
    from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
    import random
         
    runmode = TESTNET
    
    
    nodeparams = NodeParams(runmode=runmode,
                            port=8080,
                            version=60000,
                            enabledservices=SERVICES_NODE_NETWORK,
                            nonce=random.randint(0, 2**64),
                            sub_version_num="/coinpy:0.0.1/")
    presenter = CoinpyPresenter(nodeparams, ((runmode == TESTNET) and "data_testnet" or "data_main"))
    presenter.run()




        #self.mainwindow.subscribe(MainWindow.EVT_CMD_OPEN_WALLET, self.on_command_open_wallet)
        #self.client.subscribe(BitcoinClient.EVT_WALLET_OPENED, self.on_wallet_opened)
        
        #self.mainwindow.node_view.connect_to(self.client.node)
        
        #self.app.MainLoop()
