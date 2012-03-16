# -*- coding:utf-8 -*-
"""
Created on 11 Mar 2012

@author: kris
"""
import wx

class BlockchainSummaryPresenter:
    def __init__(self, blockchain, block_summary_view):
        self.block_summary_view = block_summary_view
        self.block_summary_view.set_height(str(blockchain.get_height()))

        blockchain.subscribe(blockchain.EVT_NEW_HIGHEST_BLOCK, self.on_new_highest_block)
    
        
    def on_new_highest_block(self, event):
        self.block_summary_view.set_height(str(event.height))
