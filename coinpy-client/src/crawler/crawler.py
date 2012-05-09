# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
import random
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NODE_NETWORK
from coinpy.lib.bootstrap.bootstrapper import Bootstrapper
from coinpy.model.protocol.runmode import MAIN, TESTNET
from log import createlogger
from coinpy.tools.reactor.reactor import reactor
from coinpy.node.network.bitcoin_port import BITCOIN_PORT
from coinpy.node.basic_node import BasicNode
from coinpy.node.logic.version_exchange import VersionExchangeService
from coinpy.model.protocol.messages.getaddr import GetaddrMessage
from coinpy.model.protocol.messages.types import MSG_ADDR
from coinpy.node.network.sockaddr import SockAddr
from coinpy.node.node import Node
from coinpy.tools.log.basic_logger import stdout_logger
import logging

class BitcoinCrawler():
    def __init__(self, runmode=TESTNET, seeds=[]): 
        self.log = stdout_logger(level=logging.ERROR)
        self.runmode = runmode
        nodeparams = NodeParams(runmode=runmode,
                                port=BITCOIN_PORT[runmode],
                                version=60000,
                                enabledservices=SERVICES_NODE_NETWORK,
                                nonce=random.randint(0, 2**64),
                                sub_version_num="/bitcrawler:0.1/")
        self.node = BasicNode(lambda:0, nodeparams, self.log)
        self.bootstrapper = Bootstrapper(runmode, self.log)
        
        self.node.subscribe(VersionExchangeService.EVT_VERSION_EXCHANGED, self.on_version_exchanged)
        self.node.subscribe(Node.EVT_DISCONNECTED, self.on_disconnected)
        self.node.subscribe((VersionExchangeService.EVT_MESSAGE,MSG_ADDR), self.on_addr)
        self.node.subscribe((VersionExchangeService.EVT_MESSAGE,MSG_ADDR), self.on_addr)
        self.bootstrapper.subscribe(Bootstrapper.EVT_FOUND_PEER, self.on_found_peer)

        for sockaddr in seeds:
            self.addr_pool.addpeer(sockaddr)

        self.new_addrs = set()
        self.processing_addrs = set()
        self.success_addrs = set()
        self.failed_addrs = set()        
        reactor.schedule_each(2, self.print_status)
        
    def on_addr(self, event):
        addr_msg = event.message
        for taddr in addr_msg.timenetaddr_list:
            addr = SockAddr(taddr.netaddr.ip, taddr.netaddr.port)
            if ((addr not in self.new_addrs) and (addr not in self.processing_addrs) and 
                (addr not in self.success_addrs) and (addr not in self.failed_addrs)):
                self.new_addrs.add(addr)
        #set node as processed and disconnect
        addr = event.handler.sockaddr
        if addr in self.processing_addrs:
            self.processing_addrs.remove(addr)
            self.success_addrs.add(addr)
            self.node.disconnect_peer(addr)
        self._connect_new_peers()
        
    def on_disconnected(self, event):
        addr = event.handler.sockaddr
        if addr in self.processing_addrs:
            self.processing_addrs.remove(addr)
            self.failed_addrs.add(addr)
        self._connect_new_peers()
        
    def on_found_peer(self, event):
        addr = event.peeraddress
        if ((addr not in self.new_addrs) and (addr not in self.processing_addrs) and 
            (addr not in self.success_addrs) and (addr not in self.failed_addrs)):
            self.new_addrs.add(addr)
        self._connect_new_peers()
        
    def on_version_exchanged(self, event):
        print "active peer:{id}({name}) : {ip}:{port}".format(id=event.version_message.version, name=event.version_message.sub_version_num, ip=event.handler.sockaddr.ip, port= event.handler.sockaddr.port)
        event.handler.send_message(GetaddrMessage())
     
    def _connect_new_peers(self):
        while self.new_addrs and len(self.processing_addrs) < 500:
            addr = self.new_addrs.pop()
            self.processing_addrs.add(addr)
            self.node.connect_peer(addr)
        if not self.new_addrs and not self.processing_addrs:
            print "Completed. Found {count} active peers.".format(count=len(self.success_addrs))
            reactor.stop()
            
    def print_status(self):    
        pass
        #print "Connecting:({connecting}). Remaining:({untested})".format(connecting=len(self.processing_addrs), untested=len(self.new_addrs))
          
    def on_need_peers(self, event):
        self.bootstrapper.bootstrap()
        
    def run(self):
        self.bootstrapper.bootstrap()
        reactor.run()
           


if __name__ == '__main__':
    bitcoin = BitcoinCrawler(MAIN)
    bitcoin.run()
