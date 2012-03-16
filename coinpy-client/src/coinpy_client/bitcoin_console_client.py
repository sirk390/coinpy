# -*- coding:utf-8 -*-
"""
Created on 22 Feb 2012

@author: kris
"""
 
from coinpy.model.protocol.runmode import MAIN, TESTNET
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
import random
from coinpy_client.bitcoin_client import BitcoinClient
import log

def main(runmode=TESTNET):
    data_directory = "data_testnet" if  runmode == TESTNET else "data_main"
    nodeparams = NodeParams(runmode=runmode,
                            port=8080,
                            version=60000,
                            enabledservices=SERVICES_NODE_NETWORK,
                            nonce=random.randint(0, 2**64),
                            sub_version_num="/coinpy:0.0.1/")
    
    client = BitcoinClient(log.createlogger(), nodeparams, data_directory)
    client.start()
  
if __name__ == '__main__':
    main(runmode=TESTNET)
    