# -*- coding:utf-8 -*-
"""
Created on 26 Feb 2012

@author: kris
"""
from coinpy.tools.observer import Observable
import random

class AddrPool(Observable):
    EVT_ADDED_ADDR = Observable.createevent()
    def __init__(self, reactor):
        super(AddrPool, self).__init__(reactor)
        self.known_peers = set()
        self.connecting_peers = set()
        self.connected_peers = set()
        self.failed_peers = set()
        self.banned_peers = set()
    
    def addpeer(self, sockaddr):
        if sockaddr not in self.known_peers and \
            sockaddr not in self.connecting_peers and \
            sockaddr not in self.connected_peers and \
            sockaddr not in self.failed_peers :
            #print "adding peer,", sockaddr
            self.known_peers.add(sockaddr)
            self.fire(self.EVT_ADDED_ADDR, addr=sockaddr)
        
    def failed(self, sockaddr):
        self.connecting_peers.remove(sockaddr)
        self.failed_peers.add(sockaddr)
    
    def connected(self, sockaddr):
        print "connected:", sockaddr
        self.connecting_peers.remove(sockaddr)
        self.connected_peers.add(sockaddr)
    
    def disconnected(self, sockaddr):
        self.connected_peers.remove(sockaddr)
        self.known_peers.add(sockaddr)

    def misbehaving(self, sockaddr):
        pass
    
    ''' 
        Get a peer from the addr pool.
        Returns a peer that:
            - has at least one successful connection after now-{success_since_sec}
            - has no failed connections after now-{failed_last_sec}
            - is not misbehaving
        Otherwise, returns None.
    '''
    def getpeer(self, success_since_sec=2*60*60, failed_last_sec=2*60*60):
        pass
    
    
    def getpeers(self, count):
        peers = random.sample(self.known_peers, min(count, len(self.known_peers)))
        for p in peers:
            self.known_peers.remove(p)
            self.connecting_peers.add(p)
            print "connecting:", p
        return peers
    