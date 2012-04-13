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
        #self.connecting_peers = set()
        #self.connected_peers = set()
        #self.failed_peers = set()
        self.banned_peers = set()
    
    def addpeer(self, sockaddr):
        if sockaddr not in self.known_peers and \
            sockaddr not in self.banned_peers :
            #print "adding peer,", sockaddr
            self.known_peers.add(sockaddr)
            self.fire(self.EVT_ADDED_ADDR, addr=sockaddr)
        
    def failed(self, sockaddr):
        if sockaddr in self.known_peers:
            self.known_peers.remove(sockaddr)
        #self.failed_peers.add(sockaddr)
    
    def connected(self, sockaddr):
        pass
        #self.connecting_peers.remove(sockaddr)
        #self.connected_peers.add(sockaddr)
    
    def disconnected(self, sockaddr):
        #self.connected_peers.remove(sockaddr)
        #self.known_peers.add(sockaddr)
        pass
    
    def misbehaving(self, sockaddr):
        self.known_peers.remove(sockaddr)
        self.banned_peers.add(sockaddr)
    
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
    
    def getpeers(self, count, exclude=[]):
        peers = set(random.sample(self.known_peers, min(count+len(exclude), len(self.known_peers))))
        peers -= set(exclude)
        return random.sample(peers, min(len(peers), count))
    