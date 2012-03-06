# -*- coding:utf-8 -*-
"""
Created on 21 Feb 2012

@author: kris
"""

class PoolsPresenter():
    def __init__(self, blockchain_with_pools, pools_view): 
        self.blockchain_with_pools = blockchain_with_pools
        self.pools_view = pools_view
        
        self.blockchain_with_pools.subscribe(self.blockchain_with_pools.EVT_ADDED_ORPHAN_TX, self.on_add_orphan_tx)
        self.blockchain_with_pools.subscribe(self.blockchain_with_pools.EVT_REMOVED_ORPHAN_TX, self.on_del_orphan_tx)
        self.blockchain_with_pools.subscribe(self.blockchain_with_pools.EVT_ADDED_ORPHAN_BLOCK, self.on_add_orphan_block)
        self.blockchain_with_pools.subscribe(self.blockchain_with_pools.EVT_REMOVED_ORPHAN_BLOCK, self.on_del_orphan_block)
        self.blockchain_with_pools.subscribe(self.blockchain_with_pools.EVT_ADDED_TX, self.on_add_tx)
        self.blockchain_with_pools.subscribe(self.blockchain_with_pools.EVT_REMOVED_TX, self.on_del_tx)

    def on_add_orphan_tx(self, event):
        self.pools_view.add_orphan_tx(event.hash)
        
    def on_del_orphan_tx(self, event):
        self.pools_view.del_orphan_tx(event.hash)
        
    def on_add_orphan_block(self, event):
        self.pools_view.add_orphan_block(event.hash)

    def on_del_orphan_block(self, event):
        self.pools_view.del_orphan_block(event.hash)

    def on_add_tx(self, event):
        self.pools_view.add_tx(event.hash)

    def on_del_tx(self, event):
        self.pools_view.del_tx(event.hash)

        