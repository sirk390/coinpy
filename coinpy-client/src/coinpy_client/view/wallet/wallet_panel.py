# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx
from coinpy.tools.hex import hexstr
import time
from coinpy.model.wallet.wallet_keypair import WalletKeypair
from coinpy.model.wallet.wallet_poolkey import WalletPoolKey
from coinpy.model.wallet.wallet_name import WalletName
from coinpy.tools.id_pool import IdPool
from coinpy.model.constants.bitcoin import COIN
from coinpy.tools.observer import Observable
from coinpy_client.view.wallet.send_view import SendView
from coinpy_client.view.wallet.balance import BalancePanel
from coinpy_client.view.wallet.receive_view import ReceiveView
from coinpy_client.view.wallet.enter_passphrase_view import EnterPassphraseView

class WalletPanel(wx.Panel, Observable):
    EVT_SEND = Observable.createevent()
    EVT_RECEIVE = Observable.createevent()
    EVT_SHOWHIDE_PRIVATE_KEYS = Observable.createevent()
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent) #, style=wx.SIMPLE_BORDER
        Observable.__init__(self)
        
        # Controls
        self.balance = BalancePanel(self)
        self.send_button = wx.Button(self, label="Send")
        self.receive_button = wx.Button(self, label="Receive")
        self.keylist = wx.ListCtrl(self, style=wx.LC_REPORT, size=(400,100))
        self.keylist.InsertColumn(0, "Public Key")
        self.keylist.InsertColumn(1, "Private Key")
        self.keylist.InsertColumn(2, "Address")
        self.keylist.InsertColumn(3, "Description")
        self.keylist.SetColumnWidth(2, 250)
        self.keylist.SetColumnWidth(3, 250)
        self.show_hide_private_keys_button = wx.Button(self, label="Show Hide Private Keys")
        self.txhistory_list = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.txhistory_list.InsertColumn(0, "Date")
        self.txhistory_list.InsertColumn(1, "Address")
        self.txhistory_list.InsertColumn(2, "Label")
        self.txhistory_list.InsertColumn(3, "Amount")
        self.txhistory_list.InsertColumn(4, "Confirmed")
        self.txhistory_list.SetColumnWidth(0, 120)
        self.txhistory_list.SetColumnWidth(1, 250)
        # Sizers
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.balance, 0, wx.EXPAND)
        
        send_receive_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        send_receive_sizer.Add(self.send_button, 0, wx.LEFT)
        send_receive_sizer.Add(self.receive_button, 0, wx.LEFT)
        
        self.sizer.Add(send_receive_sizer, 0, wx.EXPAND)
        self.sizer.Add(wx.StaticText(self, -1, "Keys: "), 0)
        self.sizer.Add(self.keylist, 0, wx.EXPAND)
        self.sizer.Add(self.show_hide_private_keys_button, 0)
        #self.sizer.Add(self.address_book, 0, wx.EXPAND)
        self.sizer.Add(wx.StaticText(self, -1, "Transactions: "), 0)
        self.sizer.Add(self.txhistory_list, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        # Events
        self.show_hide_private_keys_button.Bind(wx.EVT_BUTTON, self.on_show_hide_private_keys)
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send)
        self.receive_button.Bind(wx.EVT_BUTTON, self.on_receive)
        
        # ChildViews (could be moved into some View directory service)
        self.send_view = SendView(self)
        self.receive_view = ReceiveView(self)
        self.enter_passphrase_view = EnterPassphraseView(self)
        # Initialize private data
        self.keylist_idpool = IdPool()
        self.keys = {}
        self.key_itemids = {}
        
        self.itemdata_ids = IdPool()
        self.tx_history_items = {} # id => itemdata_ids
        
    def create_enter_passphrase_view(self):
        return EnterPassphraseView(self)
        
    def on_send(self, event):
        self.fire(self.EVT_SEND)

    def on_receive(self, event):
        self.fire(self.EVT_RECEIVE)
                    
    def add_key(self, id, public_key, private_key, address, description):
        itemid = self.keylist_idpool.get_id()
        self.keys[itemid] = (public_key, private_key, address, description)
        self.key_itemids[id] = itemid
        
        index = self.keylist.InsertStringItem(self.keylist.GetItemCount(), hexstr(public_key))
        self.keylist.SetItemData(index, itemid)
        self.keylist.SetStringItem(index, 1, private_key)
        self.keylist.SetStringItem(index, 2, address)
        self.keylist.SetStringItem(index, 3, description)

    def set_key_description(self, id, description):
        itemid = self.key_itemids[id]
        index = self.keylist.FindItemData(-1, itemid)
        self.keylist.SetStringItem(index, 3, description)
    
    def set_key_private_key(self, id, private_key):
        itemid = self.key_itemids[id]
        index = self.keylist.FindItemData(-1, itemid)
        self.keylist.SetStringItem(index, 1, private_key)

    def select_key(self, id):
        itemid = self.key_itemids[id]
        index = self.keylist.FindItemData(-1, itemid)
        #Deselect all
        idx = self.keylist.GetFirstSelected()
        while idx != -1:
            self.keylist.Select(index, False)
            idx =  self.keylist.GetNextSelected(idx)
        #Select and Focus
        self.keylist.Select(index)
        self.keylist.Focus(index)
        
    def add_transaction_history_item(self, id, txtime, address, label, amount, confirmed):
        itemdata = self.itemdata_ids.get_id()
        self.tx_history_items[id] = itemdata
        
        timestr = time.strftime("%Y-%m-%d %H:%m:%S", time.localtime(txtime))
        index = self.txhistory_list.InsertStringItem(self.keylist.GetItemCount(),timestr)
        self.txhistory_list.SetStringItem(index, 1, address)
        self.txhistory_list.SetStringItem(index, 2, label)
        self.txhistory_list.SetStringItem(index, 3, str(amount * 1.0 / COIN ))
        self.txhistory_list.SetStringItem(index, 4, confirmed and "Yes" or "No")
        self.txhistory_list.SetItemData(index, itemdata)
        #if (amount < 0):
        #    self.txhistory_list.SetItemBackgroundColour(index, (255, 200, 200))
        #else:
        #    self.txhistory_list.SetItemBackgroundColour(index, (200, 255, 200))
        if confirmed:
            self.txhistory_list.SetItemBackgroundColour(index, (255, 255, 255))
        else:
            self.txhistory_list.SetItemBackgroundColour(index, (255, 230, 148))  
                  
    def set_confirmed(self, id, confirmed):
        itemdata = self.tx_history_items[id]
        index = self.txhistory_list.FindItemData(-1, itemdata)
        self.txhistory_list.SetStringItem(index, 4, confirmed and "Yes" or "No")
        if confirmed:
            self.txhistory_list.SetItemBackgroundColour(index, (255, 255, 255))
        else:
            self.txhistory_list.SetItemBackgroundColour(index, (255, 230, 230))
           
    def on_show_hide_private_keys(self, event):
        self.fire(self.EVT_SHOWHIDE_PRIVATE_KEYS)
        
if __name__ == '__main__':
    from coinpy.model.protocol.runmode import MAIN, TESTNET
    wallet_filename= "D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\wallet_testnet.dat"
    wallet_filename= "D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\wallet_testnet.dat"
    
    app = wx.App(False)
    frame = wx.Frame(None)
    wallet_panel = WalletPanel(frame)
    wallet_panel.add_key("1", "public_key1", "private_key2", "adress1", "decription")
    frame.Show()
    app.MainLoop()
