# -*- coding:utf-8 -*-
"""
Created on 22 Feb 2012

@author: kris
"""
 
from coinpy.model.protocol.runmode import MAIN, TESTNET
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
import random
from coinpy_client.gui.presenter.coinpy_presenter import CoinpyPresenter
     
runmode = TESTNET
nodeparams = NodeParams(runmode=runmode,
                        port=8080,
                        version=60000,
                        enabledservices=SERVICES_NODE_NETWORK,
                        nonce=random.randint(0, 2**64),
                        sub_version_num="/coinpy:0.0.1/")
presenter = CoinpyPresenter(nodeparams, ((runmode == TESTNET) and "data_testnet" or "data_main"))
presenter.run()
