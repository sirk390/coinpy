# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.tools.observer import Observable
from coinpy.lib.bootstrap.irc_bootstrapper import IrcBootstrapper

class Bootstrapper(Observable):
    EVT_FOUND_PEER = Observable.createevent()
    
    def __init__(self, runmode, log):
        super(Bootstrapper, self).__init__()
        self.log = log  #.getChild("bootstrap")
        self.runmode = runmode
        self.ircbootstrapper = IrcBootstrapper(runmode, log=log)
        self.ircbootstrapper.subscribe(IrcBootstrapper.EVT_FOUND_PEER, self.on_found_peer)
        
    def on_found_peer(self, event):
        self.fire(self.EVT_FOUND_PEER, peeraddress=event.peeraddress)
       
    def bootstrap(self):
        self.ircbootstrapper.start()
        
