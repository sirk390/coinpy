# -*- coding:utf-8 -*-
"""
Created on 4 Mar 2012

@author: kris
"""
import random
from coinpy.model.protocol.messages.inv import InvMessage
from coinpy.model.protocol.structures.invitem import Invitem, INV_TX

"""Listen to "account" and publish new transactions on the "node".

Transactions are trickled out by selecting a random node.
trickle out tx inv: see main.cpp:2971 "Message: inventory"
"""
class TransactionPublisher():
    def __init__(self, node, account):
        self.node = node
        self.account = account
        self.account.subscribe(self.account.EVT_PUBLISH_TRANSACTION, self.on_publish_transaction)
    
    def on_publish_transaction(self, event):
        if self.node.version_service.version_exchanged_nodes:
            random_peer = random.sample(self.node.version_service.version_exchanged_nodes, 1)[0]
            if not self.node.blockchain_with_pools.contains_transaction(event.txhash):
                self.node.blockchain_with_pools.add_transaction(event.txhash, event.tx)
            self.node.send_message(random_peer, InvMessage([Invitem(INV_TX, event.txhash)]))

            