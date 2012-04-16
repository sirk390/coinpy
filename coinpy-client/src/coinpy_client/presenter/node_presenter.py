# -*- coding:utf-8 -*-
"""
Created on 22 Feb 2012

@author: kris
"""
from coinpy.node.version_exchange_node import VersionExchangeService

class NodePresenter():
    def __init__(self, node, view): 
        self.node = node
        self.view = view
        #FIXME: background thread updates the GUI here
        node.subscribe(node.EVT_CONNECTED, self.on_connected)
        node.subscribe(node.EVT_CONNECTING, self.on_connecting_peer)
        node.subscribe(node.EVT_DISCONNECTED, self.on_disconnected_peer)
        node.subscribe(VersionExchangeService.EVT_VERSION_EXCHANGED, self.on_version_exchange)
        #
        for peer in self.node.connection_manager.connecting_peers:
            self.view.add_peer(peer.sockaddr)
        for peer in self.node.connection_manager.connected_peers:
            self.view.add_peer(peer.sockaddr)
            self.view.set_peer_status(peer.sockaddr, "Connected", (230, 255, 230))
        
    def on_connecting_peer(self, event):    
        self.view.add_peer(event.handler.sockaddr)
      
    def on_connected(self, event):
        self.view.set_peer_status(event.handler.sockaddr, "Connected", (230, 255, 230))

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