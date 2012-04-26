# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""

from coinpy_client.presenter.mainwindow_presenter import MainWindowPresenter
from coinpy.tools.reactor.reactor import reactor

class CoinpyPresenter():
    def __init__(self, client, view): 
        self.client = client
        self.view = view
        self.view.subscribe(self.view.EVT_CMD_CLOSE, self.on_command_close)
        self.mainwindow_presenter = MainWindowPresenter(self.client, view.mainwindow)
      
    def on_command_close(self, event):
        reactor.stop(self.on_service_exited)
        
    def on_service_exited(self):
        self.view.stop()

    def run(self):
        self.view.start()
        reactor.run()
       
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
