# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_GETBLOCKS
from coinpy.model.protocol.messages.message import message

'''
class msg_getblocks()

Example:
    getblocks = msg_getblocks(32200, 
              [uint256.from_hexstr("000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")], #genesis
              uint256(0),
              )
    peer.send_message(getblocks)
'''
class msg_getblocks(message):
    def __init__(self, 
                 block_locator,
                 hash_stop):
        super(msg_getblocks, self).__init__(MSG_GETBLOCKS)       
        self.block_locator = block_locator
        self.hash_stop = hash_stop
        
    def __str__(self):
        return ("getblocks hash_starts(%d)[%s...], stop:%s" % (len(self.hash_starts), ",".join(str(h) for h in self.hash_starts[:5]), self.hash_stop))


