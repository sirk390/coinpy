import wx

class PoolsPanel(wx.Panel):
    def __init__(self, parent, size=(600,180)):
        super(PoolsPanel, self).__init__(parent, size=size) #, style=wx.SIMPLE_BORDER
        
        
        self.txpool_list = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.txpool_list.InsertColumn(0, "Hash")
        self.txpool_list.SetColumnWidth(0, 250)
        self.orphantx_list = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.orphantx_list.InsertColumn(0, "Hash")
        self.orphantx_list.SetColumnWidth(0, 250)
        self.orphanblocks_list = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.orphanblocks_list.InsertColumn(0, "Hash")
        self.orphanblocks_list.SetColumnWidth(0, 250)
        
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(wx.StaticText(self, -1, "Transaction Pool"))
        self.sizer.Add(self.txpool_list, 2, wx.EXPAND)
        self.sizer.Add(wx.StaticText(self, -1, "Orphan Transactions"))
        self.sizer.Add(self.orphantx_list,1, wx.EXPAND)
        self.sizer.Add(wx.StaticText(self, -1, "Orphan Blocks"))
        self.sizer.Add(self.orphanblocks_list, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        # TODO: replace FindItem's by FindItemData
        
    def add_orphan_tx(self, hash):
        self.orphantx_list.InsertStringItem(self.orphantx_list.GetItemCount(), str(hash))
        
    def del_orphan_tx(self, hash):
        index = self.orphantx_list.FindItem(-1, str(hash))
        self.orphantx_list.DeleteItem(index)
        
    def add_orphan_block(self, hash):
        self.orphanblocks_list.InsertStringItem(self.orphanblocks_list.GetItemCount(), str(hash))

    def del_orphan_block(self, hash):
        index = self.orphanblocks_list.FindItem(-1, str(hash))
        self.orphanblocks_list.DeleteItem(index)

    def add_tx(self, hash):
        self.txpool_list.InsertStringItem(self.txpool_list.GetItemCount(), str(hash))

    def del_tx(self, hash):
        index = self.txpool_list.FindItem(-1, str(hash))
        self.txpool_list.DeleteItem(index)
    
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    pools = PoolsPanel(frame)
    frame.Show()
    app.MainLoop()
