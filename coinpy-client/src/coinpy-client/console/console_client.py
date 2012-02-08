# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
import random
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
from coinpy.node.bitcoinnode import BitcoinNode
from coinpy.model.protocol.runmode import MAIN, TESTNET
import asyncore
from log import createlogger
from coinpy.model.genesis import GENESIS
from coinpy.lib.bitcoin.blockchain_with_pools import BlockchainWithPools
from coinpy.node.network.reactor import Reactor
from coinpy.lib.database.db_blockchain import BSDDbBlockChainDatabase
from coinpy.lib.bitcoin.blockchain.blockchain import Blockchain
from coinpy.node.network.sockaddr import SockAddr

class Bitcoin():
    def __init__(self, nodeparams, data_directory): 
        self.log = createlogger()
        self.nodeparams = nodeparams
        
        self.reactor = Reactor(self.log)
        self.bootstrapper = Bootstrapper(self.nodeparams.runmode, self.log)
        
        self.database = BSDDbBlockChainDatabase(self.log, self.nodeparams.runmode, directory=data_directory)
        self.database.open_or_create(GENESIS[self.nodeparams.runmode])
        self.blockchain = Blockchain(self.log, self.database)
        self.blockchain_with_pools = BlockchainWithPools(self.blockchain, self.log)
        self.node = BitcoinNode(self.reactor, self.blockchain_with_pools, self.nodeparams, self.log)
        
        self.bootstrapper.subscribe(Bootstrapper.EVT_FOUND_PEER, self.on_found_peer)
        self.node.subscribe(BitcoinNode.EVT_NEED_BOOTSTRAP, self.on_need_peers)
        
         
        self.terminate = False
        
    def on_found_peer(self, event):
        self.log.info("Found peers: %s" % (str(event.peeraddress)))
        self.node.add_peer_address(event.peeraddress)
        
    def on_need_peers(self, event):
        self.log.info("Bootstraping...")
        self.bootstrapper.bootstrap()
        
    def run(self):
        self.reactor.run()
           


if __name__ == '__main__':
    nodeparams = NodeParams(runmode=TESTNET,
                            port=8080,
                            version=32200,
                            enabledservices=SERVICES_NODE_NETWORK,
                            nonce=random.randint(0, 2**64),
                            sub_version_num="coinpy")
    bitcoin = Bitcoin(nodeparams, data_directory="data")
    bitcoin.run()