# -*- coding:utf-8 -*-
"""
Created on 16 Nov 2011

@author: kris
"""
from coinpy.node.network.lib.timeout_queue import TimeoutQueue

class DownloadStatus():
    def __init__(self):
        '''
            requested tx & blocks (using getdata)
                set of 'invitems'
        '''
        self.requested_tx = TimeoutQueue() 
        self.requested_blocks = TimeoutQueue()
        '''
            requested block hashes (using getblocks) 
        '''
        #one getblocks at a time
        self.getblocks_status = TimeoutQueue()
        
        #self.requested_getheaders = set()
