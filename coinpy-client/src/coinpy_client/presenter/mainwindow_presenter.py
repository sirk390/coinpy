# -*- coding:utf-8 -*-
"""
Created on 22 Feb 2012

@author: kris
"""
from coinpy_client.presenter.node_presenter import NodePresenter
from coinpy_client.presenter.walletbook_presenter import WalletBookPresenter
from coinpy.tools.observer import Observable
from coinpy_client.presenter.pools_presenter import PoolsPresenter
import os

class MainWindowPresenter(Observable):
    #    EVT_WALLET_OPENED = Observable.createevent()
    #Shows/hides subwindows (NodeView, WalletBook, Logs)
    def __init__(self, service, mainwindow_view):
        self.mainwindow_view = mainwindow_view
        self.service = service
        self.messages_view = self.mainwindow_view.messages_view
        
        self.node_presenter = NodePresenter(self.service.node, self.mainwindow_view.node_view)
        self.walletbook_presenter = WalletBookPresenter(self.service, self.service.wallet_set, self.mainwindow_view.nb_wallet, self.messages_view)
        self.pools_presenter = PoolsPresenter(self.service.blockchain_with_pools, self.mainwindow_view.pools_view)

        self.mainwindow_view.subscribe(self.mainwindow_view.EVT_CMD_OPEN_WALLET, self.on_open_wallet)
        
    def on_open_wallet(self, event):
        self.service.open_wallet(event.file)
       