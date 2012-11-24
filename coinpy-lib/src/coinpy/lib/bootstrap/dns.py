import socket
from coinpy.node.network.sockaddr import SockAddr
from coinpy.node.network.bitcoin_port import BITCOIN_PORT
import logging
from coinpy.tools.log.basic_logger import stdout_logger
from coinpy.node.config.nodeparams import NodeParams
from coinpy.model.protocol.services import SERVICES_NONE
import random
from coinpy.node.basic_node import BasicNode
from coinpy.node.logic.version_exchange import VersionExchangeService
from coinpy.model.protocol.messages.types import MSG_ADDR
from coinpy.model.protocol.messages.getaddr import GetaddrMessage
from coinpy.tools.observer import Observable
from coinpy.tools.reactor.reactor import reactor


class DnsBoostrapper(Observable):
    HOSTS = ["bitseed.xf2.org",
             "dnsseed.bluematt.me",
             "seed.bitcoin.sipa.be",
             "dnsseed.bitcoin.dashjr.org"]
    EVT_FOUND_PEER = Observable.createevent()

    def __init__(self, runmode, log): 
        super(DnsBoostrapper, self).__init__()
        self.log = log
        self.runmode = runmode
        nodeparams = NodeParams(runmode=runmode,
                                port=9000,
                                version=60000,
                                enabledservices=SERVICES_NONE,
                                nonce=random.randint(0, 2**64),
                                sub_version_num="/coinpy-boostrap:0.1/")
        self.node = BasicNode(lambda:0, nodeparams, self.log)
        
        self.node.subscribe(VersionExchangeService.EVT_VERSION_EXCHANGED, self.on_version_exchanged)
        self.node.subscribe((VersionExchangeService.EVT_MESSAGE,MSG_ADDR), self.on_addr)

        self.bootstrap_peers = set()
        self.peers = set()
   
    def bootstrap(self):
        for s in self.HOSTS:
            try:
                ip = socket.gethostbyname(s)
            except:
                pass
            addr = SockAddr(ip, BITCOIN_PORT[self.runmode])
            if addr not in self.bootstrap_peers:
                self.bootstrap_peers.add(addr)
                self.node.connect_peer(addr)
        
    def on_addr(self, event):
        addr_msg = event.message
        for taddr in addr_msg.timenetaddr_list:
            addr = SockAddr(taddr.netaddr.ip, taddr.netaddr.port)
            if addr not in self.peers and addr not in self.bootstrap_peers:
                self.fire(self.EVT_FOUND_PEER, peeraddress=addr)

    def on_version_exchanged(self, event):
        event.handler.send_message(GetaddrMessage())
     
      

if __name__ == '__main__':
    from coinpy.model.protocol.runmode import MAIN
    def on_found_peer(event):
        print event.peeraddress
    bootstrapper = DnsBoostrapper(MAIN, stdout_logger())
    bootstrapper.subscribe(DnsBoostrapper.EVT_FOUND_PEER, on_found_peer)
    bootstrapper.bootstrap()
    reactor.run()    