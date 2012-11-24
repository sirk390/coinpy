from coinpy.node.logic.version_exchange import VersionExchangeService

class NodePresenter():
    def __init__(self, client, view): 
        self.client = client
        self.view = view
        #FIXME: background thread updates the GUI here
        client.node.subscribe(client.node.EVT_CONNECTED, self.on_connected)
        client.node.subscribe(client.node.EVT_CONNECTING, self.on_connecting_peer)
        client.node.subscribe(client.node.EVT_DISCONNECTED, self.on_disconnected_peer)
        client.addr_pool.subscribe(client.addr_pool.EVT_ADDED_BANNED, self.on_added_banned)

        client.node.subscribe(VersionExchangeService.EVT_VERSION_EXCHANGED, self.on_version_exchange)
        #for peer in self.node.connection_manager.connecting_peers:
        #    self.view.add_peer(peer.sockaddr)
        #for peer in self.node.connection_manager.connected_peers:
        #    self.view.add_peer(peer.sockaddr)
        #    self.view.set_peer_status(peer.sockaddr, "Connected", (230, 255, 230))
        
    def on_connecting_peer(self, event):    
        self.view.add_peer(event.handler.sockaddr)
      
    def on_connected(self, event):
        if not self.view.contains_peer(event.handler.sockaddr): 
            self.view.add_peer(event.handler.sockaddr) #inbound connections are immediatly "connected"
        self.view.set_peer_status(event.handler.sockaddr, "Connected", (230, 255, 230))
    
    def on_added_banned(self, event):
        self.view.add_banned_peer(event.sockaddr, event.reason)
        
    def on_version_exchange(self, event):
        displayversion = str(event.version_message.version)
        if event.version_message.sub_version_num:
            displayversion += "(%s)" % (event.version_message.sub_version_num)
        self.view.set_peer_status(event.handler.sockaddr, "VersionExchanged", (192, 255, 192))
        self.view.set_peer_version(event.handler.sockaddr, displayversion)
        self.view.set_peer_height(event.handler.sockaddr, str(event.version_message.start_height))
      
    def on_disconnected_peer(self, event):    
        self.view.remove_peer(event.handler.sockaddr)
 
if __name__ == '__main__':
    pass