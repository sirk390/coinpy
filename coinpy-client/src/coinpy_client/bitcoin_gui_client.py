# -*- coding:utf-8 -*-
"""
Created on 22 Feb 2012

@author: kris
"""
#import warnings

#warnings.filterwarnings("error", "integer argument expected")
from coinpy.model.protocol.runmode import MAIN, TESTNET
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
import random
import coinpy_client
from coinpy_client.view.coinpy_gui import CoinpyGUI
from coinpy_client.presenter.coinpy_presenter import CoinpyPresenter
from coinpy_client.bitcoin_client import BitcoinClient
from coinpy.tools.reactor.reactor import Reactor
from coinpy_client.model.client_params import ClientParams

def main(runmode):
    data_directory = "data_testnet" if  runmode == TESTNET else "data_main"
    params = ClientParams(data_directory,
                          runmode=runmode,
                          port=8080,
                          nonce=random.randint(0, 2**64),
                          sub_version_num="/coinpy:0.0.1/",
                          targetpeers=1)
    reactor = Reactor()
    view = CoinpyGUI(reactor)
    service = BitcoinClient(reactor, view.get_logger(), params)
    presenter = CoinpyPresenter(service, view)
    presenter.run()

#testnet faucet: mhFwRrjRNt8hYeWtm9LwqCpCgXjF38RJqn

#n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo
#- Sending 1.000000 to n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo (fee:0.000000), 
#change address: mfvYfhQeKmXTKYGMUh9BJR23img6x72PYD, 
#hash:88ff0a377fcddf61c70f84c8b195d790c6809b4f54cc247a23b1d1e0fa3cdd5d
#
# old peer : 88.114.198.141:18333

if __name__ == '__main__':
    main(runmode=TESTNET)
    