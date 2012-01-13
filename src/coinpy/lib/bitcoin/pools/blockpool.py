# -*- coding:utf-8 -*-
"""
Created on 13 Dec 2011

@author: kris
"""
from coinpy.lib.bitcoin.pools.linkedblocklist import LinkedBlockList

"""
    Maintain hierarchies in a list of unordered blocks.
"""
class BlockPool():
    def __init__(self, log):
        self.log = log
        self.blocks = {}
        self.previndex = {} # { preceding_hash => LinkedBlockList, ... }
        self.endindex= {} # { last_hash => LinkedBlockList ... }

    def _update_endindex(self, oldvalue, newvalue):
        tmp = self.endindex[oldvalue]
        del self.endindex[oldvalue]
        self.endindex[newvalue] = tmp
        
    def __contains__(self, hash):  
        return hash in self.blocks

    def add_block(self, sender, hash, block):
        self.blocks[hash] = block
        if (block.blockheader.hash_prev in self.endindex):
            self.log.info("pushing back new parented:%s" % (str(hash)))
            listadded = self.endindex[block.blockheader.hash_prev]
            listadded.append_block(sender, hash, block)
            self._update_endindex(block.blockheader.hash_prev, hash)
        else:
            listadded = LinkedBlockList(sender, hash, block)
            self.previndex[block.blockheader.hash_prev] = listadded
            self.endindex[hash] = listadded
             
        #Join following list
        if (hash in self.previndex):
            self.log.info("joining lists:%s" % (str(hash)))
            listadded.append_list(self.previndex[hash])
            del self.previndex[hash]
            self._update_endindex(hash, listadded.endhash)

     
    def blocklists(self):
        return (self.previndex.values())

    def get_missing_root(self):
        if (self.previndex.values()):
            first_list =  self.previndex.values()[0]
            sender, block = first_list.blocks[0]
            return (sender, block.blockheader.hash_prev)
        return (None)
        