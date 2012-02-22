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
        self.sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.listitem_id_pool = IdPool()
        self.connections = {} # SockAddr => listitem_id
 
    def add_peer(self, sockaddr):    
        id = self.listitem_id_pool.get_id()
        self.connections[sockaddr] = id
        
        index = self.list.InsertStringItem(self.list.GetItemCount(), str(sockaddr.ip))
        self.list.SetStringItem(index, 1, str(sockaddr.port))
        self.list.SetStringItem(index, 2, "Connecting...")
        self.list.SetItemData(index, id)
                
    def set_peer_status(self, sockaddr, status, color):
        id = self.connections[sockaddr]
        index = self.list.FindItemData(-1, id)
        self.list.SetStringItem(index, 2, status)
        self.list.SetItemBackgroundColour(index, color)
        
    def set_peer_version(self, sockaddr, version):
        id = self.connections[sockaddr]
        index = self.list.FindItemData(-1, id)
        self.list.SetStringItem(index, 3, version)
        
    def remove_peer(self, sockaddr):
        id = self.connections[sockaddr]
        index = self.list.FindItemData(-1, id)
        self.list.DeleteItem(index)
        self.listitem_id_pool.release_id(id)
        del self.connections[sockaddr] 


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    NodeView(frame)
    frame.Show()
    app.MainLoop()
