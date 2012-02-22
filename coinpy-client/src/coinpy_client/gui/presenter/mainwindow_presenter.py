# -*- coding:utf-8 -*-
"""
Created on 22 Feb 2012

@author: kris
"""
from coinpy_client.gui.presenter.node_presenter import NodePresenter
from coinpy_client.gui.presenter.walletbook_presenter import WalletBookPresenter
from coinpy.tools.observer import Observable

class MainWindowPresenter(Observable):
    #    EVT_WALLET_OPENED = Observable.createevent()
    #Shows/hides subwindows (NodeView, WalletBook, Logs)
    def __init__(self, service, mainwindow_view):
        self.mainwindow_view = mainwindow_view
        self.service = service
        
        self.node_presenter = NodePresenter(self.service.node, self.mainwindow_view.node_view)
        self.walletbook_presenter = WalletBookPresenter(self.service, self.mainwindow_view.nb_wallet)
        
        
    def open_wallet(self, dbenv, filename):
        self.walletbook_presenter.open_wallet(dbenv, filename)
        
        