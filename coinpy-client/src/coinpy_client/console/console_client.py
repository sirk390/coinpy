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
from coinpy.lib.database.blockchain.db_blockchain import BSDDbBlockChainDatabase
from coinpy.lib.bitcoin.blockchain.blockchain import Blockchain
from coinpy.node.network.sockaddr import SockAddr
from coinpy.lib.bitcoin.wallet.wallet import Wallet
from coinpy.lib.database.bsddb_env import BSDDBEnv
from coinpy.node.addrpool import AddrPool
from coinpy.node.peer_reconnector import PeerReconnector
from coinpy.node.addrpool_filler import AddPoolFiller
from coinpy.tools.reactor.reactor import Reactor

class Bitcoin():
    def __init__(self, nodeparams, data_directory): 
        self.log = createlogger()
        self.nodeparams = nodeparams
        self.reactor = Reactor()
        #blockchain database
        self.bsddbenv = BSDDBEnv(directory=data_directory)
        self.database = BSDDbBlockChainDatabase(self.log, self.bsddbenv, self.nodeparams.runmode, data_directory)
        self.database.open_or_create(GENESIS[self.nodeparams.runmode])
        self.blockchain = Blockchain(self.log, self.database)
        self.blockchain_with_pools = BlockchainWithPools(self.blockchain, self.log)
        #wallet
        #self.wallet = Wallet(WalletDatabase(data_directory, "wallet.dat"), self.blockchain)
        #bootstraper
        self.bootstrapper = Bootstrapper(self.nodeparams.runmode, self.log)
        #node
        self.node = BitcoinNode(self.reactor, self.blockchain_with_pools, self.nodeparams, self.log)
        #self.node.subscribe(BitcoinNode.EVT_NEED_PEERS, self.on_need_peers)
        self.addr_pool = AddrPool()
        self.addr_pool_filler = AddPoolFiller(self.bootstrapper, self.node, self.addr_pool)
        self.peer_reconnector = PeerReconnector(self.addr_pool, self.node)
         
    def start(self):
        self.reactor.start()
           


if __name__ == '__main__':
    runmode = TESTNET
    
    
    nodeparams = NodeParams(runmode=runmode,
                            port=8080,
                            version=60000,
                            enabledservices=SERVICES_NODE_NETWORK,
                            nonce=random.randint(0, 2**64),
                            sub_version_num="/coinpy:0.0.1/")
    bitcoin = Bitcoin(nodeparams, data_directory=((runmode == TESTNET) and "data_testnet" or "data_main"))
    bitcoin.start()
