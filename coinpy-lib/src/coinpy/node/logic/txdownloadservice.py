from coinpy.model.protocol.messages.types import MSG_INV, MSG_TX
from coinpy.node.logic.version_exchange import VersionExchangeService
from coinpy.node.node import Node
from coinpy.lib.transactions.hash_tx import hash_tx
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.invitem import INV_TX
from coinpy.model.protocol.messages.getdata import GetdataMessage
from collections import deque
from coinpy.lib.blockchain.checks.tx_checks import TxVerifier
import traceback
from coinpy.tools.reactor.asynch import asynch_method

class TxDownloadService(Observable):
    EVT_ADDED_ORPHAN_TX = Observable.createevent()
    EVT_REMOVED_ORPHAN_TX = Observable.createevent()
    
    def __init__(self, node, blockchain, txpool, process_pool, log):
        Observable.__init__(self)
        self.node = node
        self.blockchain = blockchain
        self.txpool = txpool
        self.log = log
        self.items_to_download = deque()
        self.requested_tx = {}
        self.orphan_tx = {}
        self.process_pool = process_pool
        self.txverifier = TxVerifier(self.blockchain.database.runmode)
        
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_INV), self.on_inv)
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_TX), self.on_tx)
        
        self.node.subscribe (Node.EVT_DISCONNECTED, self.on_peer_disconnected)
        
    def on_inv(self, event):
        peer, message = event.handler, event.message
        for item in message.items:
            if item.type == INV_TX:
                if (not self.txpool.contains_transaction(item.hash) and 
                    not item.hash in self.requested_tx and 
                    not item.hash in self.orphan_tx):
                    self.requested_tx[item.hash] = peer
                    self.log.info("Downloading transactions from %s: %s" % (str(peer), str(item)))
                    self.node.send_message(peer, GetdataMessage([item]))
                  
    @asynch_method
    def on_tx(self, event):
        peer, message = event.handler, event.message
        hash = hash_tx(message.tx)
        self.log.info("on_tx hash:%s" % (str(hash))) 
        if (hash not in self.requested_tx):
            self.misbehaving(peer, "peer sending unrequest 'tx'")
            return
        del self.requested_tx[hash]
        #check for orphan transactions
        try:
            yield self.verified_add_tx(message.tx)
        except Exception as e:
            self.log.error("peer %s sending errorneous 'tx': %s" %(str(peer), str(e)))
            self.misbehaving(peer, "peer sending errorneous 'tx': ")
        #relay transaction
        
    def misbehaving(self, peer, reason):
        self.cleanup_peer_tasks(peer)
        self.node.misbehaving(peer, reason)

    def cleanup_peer_tasks(self, peer):
        toremove = [txhash for txhash, p in self.requested_tx.iteritems() if p==peer]
        for h in toremove:
            del self.requested_tx[txhash]
            
    def on_peer_disconnected(self, event):
        self.cleanup_peer_tasks(event.handler)

    @asynch_method
    def verified_add_tx(self, tx):
        txhash = hash_tx(tx)
        if self.txpool.contains_transaction(txhash):
            return
        self.txverifier.basic_checks(tx)
        if tx.iscoinbase():
            raise Exception("Coinbase transactions aren't allowed in memory pool")
        #check for orphan transactions.
        contains_txins = [self.blockchain.contains_transaction(txin.previous_output.hash) for txin in tx.in_list]
        if not all(contains_txins):
            self.log.info("Adding orphan tx %s" % str(txhash))
            self.orphan_tx[txhash] = tx
            self.fire(self.EVT_ADDED_ORPHAN_TX, hash=txhash)
            return
        
        self.log.info("Connecting tx %s" % str(txhash))
        self.blockchain.connect_pool_tx(tx, self.blockchain.get_height() + 1, self.process_pool)
        self.log.info("Adding tx %s" % str(tx))
        self.txpool.add_tx(txhash, tx)
        yield
