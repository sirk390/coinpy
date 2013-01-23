from coinpy.node.network.peerconnection import PeerConnection
from coinpy.tools.observer import Observable
from coinpy.node.network.sockaddr import SockAddr
from coinpy.lib.serialization.messages.s11n_message import MessageSerializer
from coinpy.tools.reactor.asyncore_plugin import AsyncorePlugin
from coinpy.tools.reactor.reactor import reactor
import traceback
import socket
from coinpy.node.network.peerhandler import PeerHandler
import asyncore

reactor.install(AsyncorePlugin())

class Node(asyncore.dispatcher, Observable):
    """Node: connect, disconnect peers, send and receive bitcoin messages. 
    
    No logic included.
    """
    EVT_NEED_PEERS = Observable.createevent()
    EVT_BASIC_MESSAGE = Observable.createevent()
    EVT_CONNECTING = Observable.createevent()
    EVT_CONNECTED = Observable.createevent()
    EVT_PEER_ERROR = Observable.createevent()
    EVT_DISCONNECTED = Observable.createevent()
    
    PEER_CONNECTING, PEER_CONNECTED, PEER_DISCONNECTING = PEER_STATES = range(3)
    
    def __init__(self, params, log):
        Observable.__init__(self)
        asyncore.dispatcher.__init__(self)
        self.params = params
        self.log = log
        
        self.message_encoder = MessageSerializer(self.params.runmode)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('localhost', self.params.port))
        self.listen(5)
        self.log.info("Listening on port :%d " % (self.params.port))
        self.peers = {}                  # addr => handler
        self.peer_states = {}            # handler => state
            
    def disconnect_peer(self, sockaddr):
        handler = self.peers[sockaddr]
        self.peer_states[handler] = Node.PEER_DISCONNECTING
        handler.clear_incomming_buffers()
        handler.handle_close()

    def connected_peer_count(self):
        return len(self.peers_with_state(Node.PEER_CONNECTED))
    
    def connecting_peer_count(self):
        return len(self.peers_with_state(Node.PEER_CONNECTING))

    def peers_with_state(self, state):
        result = []
        for peer, s in self.peer_states.iteritems():
            if s == state:
                result.append(peer)
        return result
    
    def handle_error(self):
        self.log.error(traceback.format_exc())
             
            
    def connect_peer(self, sockaddr):
        if (sockaddr in self.peers):
            raise Exception("allready connecting/connected: %s" % (str(sockaddr)))
        self.log.info("Connecting: %s" % (str(sockaddr)))
        try:
            handler = PeerConnection(sockaddr, self.message_encoder, None, log=self.log)       
        except:
            self.log.warning("Warning error connection to " + str(sockaddr))
        else:
            handler.subscribe(handler.EVT_CONNECT, self.on_peer_connected)
            handler.subscribe(handler.EVT_DISCONNECT, self.on_peer_disconnected)
            self.peers[sockaddr] = handler
            self.peer_states[handler] = Node.PEER_CONNECTING
            self.fire(self.EVT_CONNECTING, handler=handler)
        
       
    def on_peer_connected(self, event):
        self.peer_states[event.source] = Node.PEER_CONNECTED
        self.log.info("Peer Connected(%s) (peers:%d)" % ( event.source.sockaddr, self.connected_peer_count())) 
        self.fire(self.EVT_CONNECTED, handler=event.source, outbound=True)
        event.source.subscribe(PeerConnection.EVT_NEW_MESSAGE, self.__on_message)
        event.source.subscribe(PeerConnection.EVT_ERROR, self.on_error)
        

    def on_peer_disconnected(self, event):
        if self.peer_states[event.source] == Node.PEER_CONNECTED:
            self.log.info("Peer Disconnected(%s) (peers:%d)" % (str(event.source.sockaddr), self.connected_peer_count())) 
        if self.peer_states[event.source] == Node.PEER_CONNECTING:
            self.log.info("Connection Failed(%s)" % (str(event.source.sockaddr))) 
        self.fire(self.EVT_DISCONNECTED, handler=event.source)     
        del self.peers[event.source.sockaddr]
        del self.peer_states[event.source]
        
    def handle_accept(self):
        sock, (remote_ip, remote_port) = self.accept()
        remote_addr = SockAddr(remote_ip, remote_port)
        handler = PeerConnection(remote_addr, self.message_encoder, sock, self.log)
        handler.subscribe(handler.EVT_DISCONNECT, self.on_peer_disconnected)
        handler.subscribe(PeerConnection.EVT_NEW_MESSAGE, self.__on_message)
        handler.subscribe(PeerConnection.EVT_ERROR, self.on_error)
        self.peers[remote_addr] = handler
        self.peer_states[handler] = Node.PEER_CONNECTED
        self.log.info("Peer Accepted(%s) (peers:%d)" % ( remote_addr, self.connected_peer_count())) 
        self.fire(self.EVT_CONNECTED, handler=handler, outbound=False)

    def send_message(self, peer, message):
        peer.send_message(message)

    def __on_message(self, event):
        handler, message = event.handler, event.message
        self.fire(self.EVT_BASIC_MESSAGE, message=message, handler=handler)

    def on_error(self, event):
        handler, error = event.handler, event.error
        self.fire(self.EVT_PEER_ERROR, error=error, handler=handler)


