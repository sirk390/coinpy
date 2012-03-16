# -*- coding:utf-8 -*-
"""
Created on 9 Mar 2012

@author: kris
"""
import wx
from coinpy.lib.bitcoin.hash_block import hash_block
from coinpy.model.protocol.runmode import MAIN
 
#present a BlockSummary() instead of a block
# BlockSummary contains also hash_next and height
class BlockPresenter():
    def __init__(self, block, block_view):
        block_view.set_hash(hash_block(block).get_hexstr())
        block_view.set_previous_block(block.blockheader.hash_prev.get_hexstr())
    
if __name__ == '__main__':
    from coinpy_client.view.blockchain.block_view import BlockView
    from coinpy.model.genesis import GENESIS

    app = wx.App(False)
    frame = wx.Frame(None, size=(500, 600))
    view = BlockView(frame)
    BlockPresenter(GENESIS[MAIN], view)
    
    frame.Show()
    app.MainLoop()