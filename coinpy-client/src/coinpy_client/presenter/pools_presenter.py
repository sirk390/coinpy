
class PoolsPresenter():
    def __init__(self, node, pools_view): 
        self.node = node
        self.pools_view = pools_view
        
        self.node.txdl.subscribe(self.node.txdl.EVT_ADDED_ORPHAN_TX, self.on_add_orphan_tx)
        self.node.txdl.subscribe(self.node.txdl.EVT_REMOVED_ORPHAN_TX, self.on_del_orphan_tx)
        self.node.blockdl.orphanblocks.subscribe(self.node.blockdl.orphanblocks.EVT_ADDED_ORPHAN_BLOCK, self.on_add_orphan_block)
        self.node.blockdl.orphanblocks.subscribe(self.node.blockdl.orphanblocks.EVT_REMOVED_ORPHAN_BLOCK, self.on_del_orphan_block)
        self.node.txpool.subscribe(self.node.txpool.EVT_ADDED_TX, self.on_add_tx)
        self.node.txpool.subscribe(self.node.txpool.EVT_REMOVED_TX, self.on_del_tx)

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

        