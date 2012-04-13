# -*- coding:utf-8 -*-
"""
Created on 22 Feb 2012

@author: kris
"""
from coinpy_client.presenter.node_presenter import NodePresenter
from coinpy.tools.observer import Observable
from coinpy_client.presenter.pools_presenter import PoolsPresenter
import os
from coinpy_client.presenter.blockchain.blockchain_summary_presenter import BlockchainSummaryPresenter
from coinpy_client.presenter.accountbook_presenter import AccountBookPresenter
import traceback

class MainWindowPresenter(Observable):
    #    EVT_WALLET_OPENED = Observable.createevent()
    #Shows/hides subwindows (NodeView, WalletBook, Logs)
    def __init__(self, service, mainwindow_view):
        self.mainwindow_view = mainwindow_view
        self.service = service
        self.messages_view = self.mainwindow_view.messages_view
        
        self.node_presenter = NodePresenter(self.service.node, self.mainwindow_view.node_view)
        self.walletbook_presenter = AccountBookPresenter(self.service, self.service.account_set, self.mainwindow_view.nb_wallet, self.messages_view)
        self.pools_presenter = PoolsPresenter(self.service.blockchain_with_pools, self.mainwindow_view.pools_view)
        self.blockchain_summary_presenter = BlockchainSummaryPresenter(self.service.blockchain_with_pools.blockchain, self.mainwindow_view.blockchain_summary_view)
        self.mainwindow_view.subscribe(self.mainwindow_view.EVT_CMD_OPEN_WALLET, self.on_cmd_open_wallet)
        self.mainwindow_view.subscribe(self.mainwindow_view.EVT_CMD_CLOSE_WALLET, self.on_cmd_close_wallet)
        
        
    def on_cmd_open_wallet(self, event):
        try:
            self.service.open_wallet(event.file)
        except Exception as exc:
            traceback.print_exc()
            self.mainwindow_view.messages_view.error(str(exc))

    def on_cmd_close_wallet(self, event):
        self.service.close_wallet(event.id)
        