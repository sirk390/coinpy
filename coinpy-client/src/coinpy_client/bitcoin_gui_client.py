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

def main(runmode):
    data_directory = "data_testnet" if  runmode == TESTNET else "data_main"
    params = ClientParams(data_directory,
                          runmode=runmode,
                          port=8333,
                          nonce=random.randint(0, 2**64),
                          sub_version_num="/coinpy:0.0.1/",
                          targetpeers=10)
    view = CoinpyGUI()
    client = BitcoinClient(view.get_logger(), params)
    presenter = CoinpyPresenter(client, view)
    presenter.run()

#testnet faucet: mhFwRrjRNt8hYeWtm9LwqCpCgXjF38RJqn

# old peer : 88.114.198.141:18333

if __name__ == '__main__':
    main(runmode=TESTNET)
    