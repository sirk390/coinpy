# -*- coding:utf-8 -*-
"""
Created on 6 May 2012

@author: kris
"""
from coinpy.model.protocol.messages.types import MSG_INV, MSG_TX
from coinpy.node.logic.version_exchange import VersionExchangeService
from coinpy.node.node import Node
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.invitem import INV_TX
from coinpy.model.protocol.messages.getdata import GetdataMessage
from collections import deque
from coinpy.lib.bitcoin.checks.tx_checks import TxVerifier
import traceback
from coinpy.tools.reactor.asynch import asynch_method

class TxDownloadService(Observable):
    EVT_ADDED_ORPHAN_TX = Observable.createevent()
    EVT_REMOVED_ORPHAN_TX = Observable.createevent()
    
    def __init__(self, node, blockchain, txpool, log):
        Observable.__init__(self)
        self.node = node
        self.blockchain = blockchain
        self.txpool = txpool
        self.log = log
        self.items_to_download = deque()
        self.requested_tx = {}
        self.txverifier = TxVerifier(self.blockchain.database.runmode)
        
    def install(self, node):
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_INV), self.on_inv)
        node.subscribe((VersionExchangeService.EVT_MESSAGE, MSG_TX), self.on_tx)
        
        self.node.subscribe (Node.EVT_DISCONNECTED, self.on_peer_disconnected)
        
    def on_inv(self, event):
        peer, message = event.handler, event.message
        for item in message.items:
            if item.type == INV_TX:
                if (not self.txpool.contains_transaction(item.hash) and not
                    item.hash in self.requested_tx):
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
        try:
            yield self.verified_add_tx(message.tx)
        except Exception as e:
            self.log.error("peer sending errorneous 'tx':" + str(e))
            self.misbehaving(peer, "peer sending errorneous 'tx': ")
            
    def on_peer_disconnected(self, event):
        pass
    
    @asynch_method
    def verified_add_tx(self, tx):
        txhash = hash_tx(tx)
        if self.txpool.contains_transaction(txhash):
            return
        self.txverifier.basic_checks(tx)
        if tx.iscoinbase():
            raise Exception("Coinbase transactions aren't allowed in memory pool")
        self.log.info("Connecting tx %s" % str(txhash))
        yield self.blockchain._connect_tx(tx, self.blockchain.get_height() + 1, False)
        #todo: 1/check for conflicts / replace transactions
        
        # 2/check for non-standard pay-to-script-hash in inputs
        # 3/check minimum fees
        self.log.info("Adding tx %s" % str(tx))
        self.txpool.add_tx(txhash, tx)
        