# -*- coding:utf-8 -*-
"""
Created on 22 Feb 2012

@author: kris
"""
#import warnings

#warnings.filterwarnings("error", "integer argument expected")
from coinpy.model.protocol.runmode import MAIN, TESTNET
import random
from coinpy_client.view.coinpy_gui import CoinpyGUI
from coinpy_client.presenter.coinpy_presenter import CoinpyPresenter
from coinpy_client.bitcoin_client import BitcoinClient
from coinpy_client.model.client_params import ClientParams
from coinpy.node.network.bitcoin_port import BITCOIN_PORT
from coinpy.node.network.sockaddr import SockAddr
from coinpy_client.config_params import get_config_params

def coinpy_gui_client(client_params):
    view = CoinpyGUI()
    client = BitcoinClient(view.get_logger(), client_params)
    presenter = CoinpyPresenter(client, view)
    presenter.run()

if __name__ == '__main__':

    #testnet faucet: mhFwRrjRNt8hYeWtm9LwqCpCgXjF38RJqn
    # old peer : 88.114.198.141:18333
    runmode=TESTNET
    data_directory = "data_testnet" if  runmode == TESTNET else "data_main"
    params = ClientParams(runmode=runmode, 
                          data_directory=data_directory,
                          findpeers=True,
                          seeds=[SockAddr("127.0.0.1", 7000)])
    coinpy_gui_client(get_config_params(params))

