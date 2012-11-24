import wx
import wx.lib.agw.hyperlink as hyperlink

class TransactionView(wx.Panel):
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent)
        # Styles
        font_large = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        font_bold = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        txtctrl_style = wx.TE_READONLY|wx.BORDER_SIMPLE #|wx.TE_RIGHT
        txtctrl_color = (196,196,196)
        # Controls
        self.transaction_label = wx.StaticText(self, -1, "Transaction", size=(350,-1))
        self.transaction_label.SetFont(font_large)
        
        self.location_label = wx.StaticText(self, -1, "Location:")
        self.location_textctrl = wx.TextCtrl(self, -1, "", size=(150,-1), style=txtctrl_style)
        self.location_textctrl.SetBackgroundColour(txtctrl_color)
        self.depth_label = wx.StaticText(self, -1, "Depth:")
        self.depth_textctrl = wx.TextCtrl(self, -1, "", size=(150,-1), style=txtctrl_style)
        self.depth_textctrl.SetBackgroundColour(txtctrl_color)
        self.block_label = wx.StaticText(self, -1, "Block:")
        self.block_hyperlink =  hyperlink.HyperLinkCtrl(self, wx.ID_ANY, "")
        self.amount_label = wx.StaticText(self, -1, "Amount:")
        self.amount_textctrl = wx.TextCtrl(self, -1, "", size=(150,-1), style=txtctrl_style)
        self.amount_textctrl.SetBackgroundColour(txtctrl_color)
        self.fee_label = wx.StaticText(self, -1, "Fee:")
        self.fee_textctrl = wx.TextCtrl(self, -1, "", size=(150,-1), style=txtctrl_style)
        self.fee_textctrl.SetBackgroundColour(txtctrl_color)
        self.type_label = wx.StaticText(self, -1, "Type:")
        self.type_textctrl = wx.TextCtrl(self, -1, "", size=(150,-1), style=txtctrl_style)
        self.type_textctrl.SetBackgroundColour(txtctrl_color)
        
        self.inputs_label = wx.StaticText(self, -1, "Inputs", size=(350,-1))
        self.inputs_label.SetFont(font_bold)
        self.inputs_listctrl = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.inputs_listctrl.InsertColumn(0, "Hash")
        self.inputs_listctrl.InsertColumn(1, "Index")
        self.inputs_listctrl.InsertColumn(2, "Amount")
        self.inputs_listctrl.InsertColumn(3, "Script")
        self.inputs_listctrl.InsertColumn(4, "Redeem Script")
        
        self.outputs_label = wx.StaticText(self, -1, "Ouputs", size=(350,-1))
        self.outputs_label.SetFont(font_bold)
        self.outputs_listctrl = wx.ListCtrl(self,style=wx.LC_REPORT, size=(400,100))
        self.outputs_listctrl.InsertColumn(0, "Script")
        self.outputs_listctrl.InsertColumn(1, "Amount")
      
        #Sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        formsizer = wx.FlexGridSizer(7, 2, vgap=2)
        formsizer.Add(self.location_label, 0)
        formsizer.Add(self.location_textctrl, 0)
        formsizer.Add(self.depth_label, 0)
        formsizer.Add(self.depth_textctrl, 0)
        formsizer.Add(self.block_label, 0)
        formsizer.Add(self.block_hyperlink, 0)
        formsizer.Add(self.amount_label, 0)
        formsizer.Add(self.amount_textctrl, 0)
        formsizer.Add(self.fee_label, 0)
        formsizer.Add(self.fee_textctrl, 0)
        formsizer.Add(self.type_label, 0)
        formsizer.Add(self.type_textctrl, 0)
        
        self.sizer.Add(self.transaction_label, 0)
        self.sizer.Add(formsizer, 0, wx.EXPAND)
        self.sizer.Add(self.inputs_label, 0)
        self.sizer.Add(self.inputs_listctrl,  0, wx.EXPAND)
        self.sizer.Add(self.outputs_label)
        self.sizer.Add(self.outputs_listctrl,  0, wx.EXPAND)
        self.SetSizer(self.sizer)
        
    def set_location(self, location):
        self.location_textctrl.SetValue(location)
        
    def set_depth(self, depth):
        self.depth_textctrl.SetValue(depth)
        
    def set_blockhash(self, blockhash):
        self.block_hyperlink.SetLabel(blockhash)
        
    def set_amount(self, amount):
        self.amount_textctrl.SetValue(amount)
        
    def set_fee(self, fee):
        self.fee_textctrl.SetValue(fee)
        
    def set_type(self, txtype):
        self.type_textctrl.SetValue(txtype)
        
    def add_input(self, txhash, txindex, script, redeem_script, amount):
        index = self.inputs_listctrl.InsertStringItem(self.inputs_listctrl.GetItemCount(), txhash)
        self.inputs_listctrl.SetStringItem(index, 1, txindex)
        self.inputs_listctrl.SetStringItem(index, 2, amount)
        self.inputs_listctrl.SetStringItem(index, 3, script)
        self.inputs_listctrl.SetStringItem(index, 4, redeem_script)

    def add_output(self, script, amount):
        index = self.outputs_listctrl.InsertStringItem(self.outputs_listctrl.GetItemCount(), script)
        self.outputs_listctrl.SetStringItem(index, 1, amount)

        
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, size=(500, 600))
    TransactionView(frame)


    frame.Show()
    app.MainLoop()