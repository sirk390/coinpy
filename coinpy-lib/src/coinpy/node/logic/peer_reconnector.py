import time
from coinpy.node.node import Node

"""
check supported version?
        if (not self.is_supported_version(event.message.version)):
            self.log.warning("version %d not supported" % (event.message.version))
            self.node.misbehaving(event.handler, "version %d not supported" % (event.message.version))
            return

"""
class PeerReconnector():
    def __init__(self, log, node, addrpool, min_connections=4):
        self.log = log
        self.addrpool = addrpool
        self.min_connections = min_connections
        self.connecting_peers = set()
        
        self.node = node
        self.node.subscribe(self.node.EVT_CONNECTED, self.on_peer_connected)
        self.node.subscribe(self.node.EVT_PEER_ERROR, self.on_peer_error)
        self.node.subscribe(self.node.EVT_DISCONNECTED, self.on_peer_disconnected)
        self.addrpool.subscribe(self.addrpool.EVT_ADDED_ADDR, self.on_added_addr)
        self.check_connection_count()


           
    def on_peer_connected(self, event):
        self.addrpool.log_success(time.time(), event.handler.sockaddr)
        if event.handler.sockaddr in self.connecting_peers: #not true for inbound connections
            self.connecting_peers.remove(event.handler.sockaddr)
    
    def on_peer_error(self, event):
        self.log.info("Banning peer %s for err '%s'" %(str(event.handler.sockaddr), str(event.error)))
        self.addrpool.misbehaving(event.handler.sockaddr, event.error)
        if (event.handler in self.node.peers and
            self.node.peer_states[event.handler] != Node.PEER_DISCONNECTING): # might allready be disconnecting (if 2 errors follow each other closely)
            self.log.info("Banning peer %s for error '%s'" %(str(event.handler.sockaddr), str(event.error)))
            self.node.disconnect_peer(event.handler.sockaddr)
    
    def on_peer_disconnected(self, event):
        addr = event.handler.sockaddr
        if addr in self.connecting_peers:
            self.addrpool.log_failure(time.time(), addr)
        self.check_connection_count()
            
    def check_connection_count(self):
        missing_count = int(self.min_connections - \
                        self.node.connected_peer_count() \
                        - (self.node.connecting_peer_count() / 2.0))
                        
        if missing_count > 0:
            connected_or_connecting = set(self.node.peers)
            peeraddrs = self.addrpool.getpeers(missing_count, exclude=connected_or_connecting)
            for peeraddr in peeraddrs:
                self.node.connect_peer(peeraddr)
                self.connecting_peers.add(peeraddr)
                
    def on_added_addr(self, event):
        self.check_connection_count()
        
        