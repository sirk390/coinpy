import asyncore
import socket
import time
from peerhandler import PeerHandler
import traceback
from peerconnection import PeerConnection
from coinpy.tools.observer import Observable
from coinpy.model.protocol.messages.getaddr import msg_getaddr
from coinpy.node.network.sockaddr import SockAddr

PEER_RECONNECT_INTERVAL = 5

class ConnectionManager(asyncore.dispatcher, Observable):
    EVT_ADDED_HANDLER = Observable.createevent()
    EVT_REMOVED_HANDLER = Observable.createevent()
    EVT_CONNECTED_HANDLER = Observable.createevent()
    EVT_DISCONNECTED_HANDLER = Observable.createevent()

    def __init__(self, reactor, sockaddr, connection_factory, log):
        Observable.__init__(self)
        asyncore.dispatcher.__init__(self)
        self.log = log
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((sockaddr.ip, sockaddr.port))
        self.listen(5)
        
        self.known_peer_addresses = set()
        
        self.peers = {}               # addr => handler
        self.connecting_peers = set() # set(handler,...)
        self.connected_peers = set()  # set(handler,...)
        
        self.connection_factory = connection_factory
        self.reactor = reactor
        self.reactor.schedule_each(1, self.reconnect_peers)
       
    def add_peer_address(self, addr):
        self.known_peer_addresses.add(addr)
            
    def remove_peer(self, addr, close=True):
        if (close and (addr in self.peers)):
            handler = self.peers[addr]
            handler.handle_close()
        #print self.known_peer_addresses.pop() == addr
        print addr
        self.known_peer_addresses.remove(addr)

    def handle_error(self):
        self.log.error(traceback.format_exc())
             
    def reconnect_peers(self):
        for addr in self.known_peer_addresses:
            if addr not in self.peers:
                self._connect_peer(addr)
            
    def _connect_peer(self, sockaddr):
        self.log.info("Connecting: %s" % (str(sockaddr)))
        handler = self.connection_factory.create_connection(sockaddr)        
        handler.subscribe(handler.EVT_CONNECT, self.on_peer_connected)
        handler.subscribe(handler.EVT_DISCONNECT, self.on_peer_disconnected)
        self.peers[sockaddr] = handler
        self.connecting_peers.add(handler)
        self.fire(self.EVT_ADDED_HANDLER, handler=handler)

       
    def on_peer_connected(self, event):
        self.connecting_peers.remove(event.source)
        self.connected_peers.add(event.source)
        self.log.info("Peer Connected(%s) (peers:%d)" % ( event.source.sockaddr, len(self.connected_peers))) 
        self.fire(self.EVT_CONNECTED_HANDLER, handler=event.source, outbound=True)

    def on_peer_disconnected(self, event):
        if event.source in self.connected_peers:
            self.connected_peers.remove(event.source)
            self.fire(self.EVT_DISCONNECTED_HANDLER, handler=event.source)
        if event.source in self.connecting_peers:
            self.connecting_peers.remove(event.source)       
        del self.peers[event.source.sockaddr]
        self.log.info("Peer Disconnected(%s) (peers:%d)" % (str(event.source.sockaddr), len(self.connected_peers))) 
        self.fire(self.EVT_REMOVED_HANDLER, handler=event.source)
        
    def handle_accept(self):
        pair = self.accept()
        sock, addr = pair
        handler = self.connection_factory.create_connection(SockAddr(sock, addr))
        handler.subscribe(handler.EVT_DISCONNECT, self.on_peer_disconnected)
        self.connected_peers.add(handler)
        self.fire(self.EVT_CONNECTED_HANDLER, handler=handler, outbound=False)


if __name__ == '__main__':
    
    server = ConnectionManager('localhost', 8080)
    
    #knownpeers = [('180.219.13.116', 18333), ('88.77.85.132', 18333), ('84.189.40.74', 18333), ('109.169.54.178', 18333), ('188.120.137.114', 18333), ('24.7.159.169', 18333), ('115.64.155.43', 18333), ('91.65.176.70', 18333), ('80.203.26.133', 18333), ('173.79.80.45', 18333), ('88.198.7.53', 18333), ('64.62.190.127', 18333), ('50.57.76.16', 18333), ('199.199.210.202', 18333), ('74.118.73.101', 18333), ('81.56.46.96', 18333), ('83.243.59.59', 18333), ('193.254.191.71', 18333), ('216.223.156.181', 18333), ('66.197.184.28', 18333), ('212.32.186.86', 18333), ('87.79.73.36', 18333), ('129.177.17.64', 18333), ('172.17.2.157', 18333), ('98.210.99.53', 18333), ('66.228.44.77', 18333), ('213.133.150.161', 18333), ('193.254.191.233', 18333), ('65.49.26.16', 18333), ('79.120.12.63', 18333), ('85.10.226.132', 18333), ('78.46.58.142', 18333), ('216.47.50.24', 18333), ('212.32.186.201', 18333), ('194.38.107.23', 18333), ('80.81.243.239', 18333), ('188.138.101.169', 18333), ('188.165.213.169', 18333), ('50.17.79.122', 18333), ('212.201.77.52', 18333), ('46.137.6.83', 18333), ('66.9.24.5', 18333), ('204.11.247.39', 18333), ('217.142.134.19', 18333), ('213.21.81.169', 18333), ('69.164.218.197', 18333), ('94.125.73.150', 18333), ('77.37.6.11', 18333), ('46.4.245.112', 18333)]
    knownpeers = [SockAddr('88.198.7.53', 18333), SockAddr('83.243.59.59', 18333), SockAddr('85.10.226.132', 18333)]
    # ('78.46.58.142', 18333), ('188.138.101.169', 18333)]
    for p in knownpeers:
        server.add_known_peer_address(p)
    server.mainloop()

