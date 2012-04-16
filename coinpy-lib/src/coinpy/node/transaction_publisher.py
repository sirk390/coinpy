# -*- coding:utf-8 -*-
"""
Created on 4 Mar 2012

@author: kris
"""
# TransactionPublisher
#     Puts transactions in the wallet, relays unconfirmed wallet transactions to
#     the node trickler. 
import random
from coinpy.model.protocol.messages.inv import msg_inv
from coinpy.model.protocol.structures.invitem import invitem, INV_TX

class TransactionPublisher():
    def __init__(self, reactor, node, account):
        self.reactor = reactor
        self.node = node
        self.account = account
        self.account.subscribe(self.account.EVT_PUBLISH_TRANSACTION, self.on_publish_transaction)
    
    def on_publish_transaction(self, event):
        #trickle out tx inv, see main.cpp:2971 "Message: inventory"
        if self.node.version_service.version_exchanged_nodes:
            random_peer = random.sample(self.node.version_service.version_exchanged_nodes, 1)[0]
            if not self.node.blockchain_with_pools.contains_transaction(event.txhash):
                self.node.blockchain_with_pools.add_transaction(event.txhash, event.tx)
            self.node.send_message(random_peer, msg_inv([invitem(INV_TX, event.txhash)]))

            