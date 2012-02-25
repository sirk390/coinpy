# -*- coding:utf-8 -*-
"""
Created on 14 Feb 2012

@author: kris
"""
import wx
from coinpy_client.gui.view.wallet.balance import BalancePanel
from coinpy_client.gui.view.wallet.address_book_panel import AddressBookPanel
from coinpy_client.gui.view.wallet.transations_panel import TransactionsPanel
from coinpy.tools.hex import hexstr
from coinpy_client.gui.view.wallet.send_receive_panel import SendReceivePanel
from coinpy.lib.database.bsddb_env import BSDDBEnv
import time
from coinpy.lib.database.blockchain.db_blockchain import BSDDbBlockChainDatabase
from coinpy.lib.bitcoin.wallet.wallet_balance import WalletBalance
from coinpy.model.wallet.wallet_keypair import WalletKeypair
from coinpy.model.wallet.wallet_poolkey import WalletPoolKey
from coinpy.model.wallet.wallet_name import WalletName
from coinpy.tools.id_pool import IdPool
from coinpy.model.constants.bitcoin import COIN

class WalletPanel(wx.Panel):
    def __init__(self, parent):
        super(WalletPanel, self).__init__(parent) #, style=wx.SIMPLE_BORDER
        
        self.balance = BalancePanel(self)
        self.send_receive = SendReceivePanel(self)
        self.keylist = wx.ListCtrl(self, style=wx.LC_REPORT, size=(400,100))
        self.keylist.InsertColumn(0, "Public Key")
        self.keylist.InsertColumn(1, "Private Key")
        self.keylist.InsertColumn(2, "Pool")
        self.keylist.InsertColumn(3, "Pool Time")
        self.keylist.InsertColumn(4, "Address")
        self.keylist.InsertColumn(5, "Name")
        self.show_hide_private_keys_button = wx.Button(self, label="Show Private Keys")
        
        self.txhistory_list = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.txhistory_list.InsertColumn(0, "Date")
        self.txhistory_list.InsertColumn(1, "Address")
        self.txhistory_list.InsertColumn(2, "Label")
        self.txhistory_list.InsertColumn(3, "Amount")
        self.txhistory_list.SetColumnWidth(0, 120)
        self.txhistory_list.SetColumnWidth(1, 250)
        
        
        #self.address_book = AddressBookPanel(self)
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.balance, 0, wx.EXPAND)
        self.sizer.Add(self.send_receive, 0, wx.EXPAND)
        self.sizer.Add(wx.StaticText(self, -1, "Keys: "), 0)
        self.sizer.Add(self.keylist, 0, wx.EXPAND)
        self.sizer.Add(self.show_hide_private_keys_button, 0)
        #self.sizer.Add(self.address_book, 0, wx.EXPAND)
        self.sizer.Add(wx.StaticText(self, -1, "Transactions: "), 0)
        self.sizer.Add(self.txhistory_list, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.show_hide_private_keys_button.Bind(wx.EVT_BUTTON, self.on_show_hide_private_keys)
        self.show_private_keys = False
        
        self.keylist_idpool = IdPool()
        self.keys = {}
        
    def add_key(self, key, poolkey, name):
        id = self.keylist_idpool.get_id()
        self.keys[id] = (key, poolkey, name)
        
        index = self.keylist.InsertStringItem(self.keylist.GetItemCount(), hexstr(key.public_key))
        self.keylist.SetItemData(index, id)
        self.keylist.SetStringItem(index, 1, self.private_key_mask(hexstr(key.private_key)))
        if poolkey:
            self.keylist.SetStringItem(index, 2, "%d" % (poolkey.poolnum))
            timestr = time.strftime("%Y-%m-%d %H:%m:%S", time.gmtime(poolkey.time))
            self.keylist.SetStringItem(index, 3, timestr)
        if name:
            self.keylist.SetStringItem(index, 4, name.address)
            self.keylist.SetStringItem(index, 5, name.name)


    def add_transaction_history_item(self, txtime, address, label, amount):
        timestr = time.strftime("%Y-%m-%d %H:%m:%S", time.localtime(txtime))
        index = self.txhistory_list.InsertStringItem(self.keylist.GetItemCount(),timestr)
        self.txhistory_list.SetStringItem(index, 1, address)
        self.txhistory_list.SetStringItem(index, 2, label)
        self.txhistory_list.SetStringItem(index, 3, str(amount * 1.0 / COIN ))
        if (amount < 0):
            self.txhistory_list.SetItemBackgroundColour(index, (255, 200, 200))
        else:
            self.txhistory_list.SetItemBackgroundColour(index, (200, 255, 200))
            
    def private_key_mask(self, private_key):
        return (private_key if self.show_private_keys else "***" )
    
    def on_show_hide_private_keys(self, event):
        self.show_private_keys = not self.show_private_keys
        for i in range(self.keylist.GetItemCount()):
            id = self.keylist.GetItemData(i)
            key, _, _ = self.keys[id]
            self.keylist.SetStringItem(i, 1,self.private_key_mask(hexstr(key.private_key)))
        button_label = ("Hide" if self.show_private_keys else "Show") + " Private Keys"
        self.show_hide_private_keys_button.SetLabel(button_label) 
        
if __name__ == '__main__':
    from coinpy.model.protocol.runmode import MAIN, TESTNET
    wallet_filename= "D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\wallet_testnet.dat"
    wallet_filename= "D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\wallet_testnet.dat"
    
    app = wx.App(False)
    frame = wx.Frame(None)
    wallet_panel = WalletPanel(frame)
    wallet_panel.add_key(WalletKeypair("public_key1", "private_key2"), 
                         WalletPoolKey(3, 3, time.time(), "public_key1"),
                         WalletName("name1", "adress1"))
    frame.Show()
    app.MainLoop()
