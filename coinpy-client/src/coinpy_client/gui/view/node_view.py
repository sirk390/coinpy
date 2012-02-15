# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx
from coinpy.node.node import Node
from coinpy.tools.id_pool import IdPool
from coinpy.node.version_exchange_node import VersionExchangeNode

class NodeView(wx.Panel):
    def __init__(self, parent):
        super(NodeView, self).__init__(parent, size=(380,600))
        
        self.list = wx.ListCtrl(self,style=wx.LC_REPORT)
        self.list.InsertColumn(0, "ip")
        self.list.SetColumnWidth(0, 80)
        self.list.InsertColumn(1, "port")
        self.list.SetColumnWidth(1, 50)
        self.list.InsertColumn(2, "status")
        self.list.SetColumnWidth(2, 80)
        self.list.InsertColumn(3, "version")
        self.list.SetColumnWidth(3, 80)
        
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        #self.sizer.Add(wx.StaticText(self, -1, "Keys: "))
        self.sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.listitem_id_pool = IdPool()
        self.connections = {} # SockAddr => listitem_id
        
    def connect_to(self, node): 
        node.subscribe(Node.EVT_CONNECTED, self.on_connected)
        node.subscribe(Node.EVT_ADDED_PEER, self.on_added_peer)
        node.subscribe(Node.EVT_REMOVED_PEER, self.on_removed_peer)
        node.subscribe(VersionExchangeNode.EVT_VERSION_EXCHANGED, self.on_version_exchange)

    def on_added_peer(self, event):    
        id = self.listitem_id_pool.get_id()
        self.connections[event.handler.sockaddr] = id
        
        index = self.list.InsertStringItem(0, str(event.handler.sockaddr.ip))
        self.list.SetStringItem(index, 1, str(event.handler.sockaddr.port))
        self.list.SetStringItem(index, 2, "Connecting...")
        self.list.SetItemData(index, id)
                
    def on_connected(self, event):
        id = self.connections[event.handler.sockaddr]
        index = self.list.FindItemData(-1, id)
        print "Connected %s (id:%d, index:%d)" % (str(event.handler.sockaddr), id, index)
        self.list.SetStringItem(index, 2, "Connected")
        
        self.list.SetItemBackgroundColour(index, (230, 255, 230))
        
    def on_version_exchange(self, event):
        id = self.connections[event.handler.sockaddr]
        index = self.list.FindItemData(-1, id)
        self.list.SetStringItem(index, 2, "VersionExchanged")
        displayversion = str(event.version_message.version)
        if event.version_message.sub_version_num:
            displayversion += "(%s)" % (event.version_message.sub_version_num)
        self.list.SetStringItem(index, 3, displayversion)
        self.list.SetItemBackgroundColour(index, (192, 255, 192))
        #print index
        #print "Connected, " + str(event.handler.sockaddr)
        #index = self.keys.list.InsertStringItem(0, hexstr(k.public_key))
        #self.keys.list.SetStringItem(index, 1, hexstr(k.private_key))
            
    def on_removed_peer(self, event):
        id = self.connections[event.handler.sockaddr]
        index = self.list.FindItemData(-1, id)
        self.list.DeleteItem(index)
        self.listitem_id_pool.release_id(id)
        del self.connections[event.handler.sockaddr] 
        print "Disconnected %s (id:%d, index:%d)" % (str(event.handler.sockaddr), id, index)
        