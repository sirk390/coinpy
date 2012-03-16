# -*- coding:utf-8 -*-
"""
Created on 15 Feb 2012

@author: kris
"""
import time

"""
     WalletTx:    A transaction with metadata as saved in the wallet
         merkle_tx: (MerkleTx) the transaction 
         map_value: {key => value} map for saving metadata information.
                     recognized keys: 
                         "fromaccount", account name for JSON-RPC, default=empty
                         "spent" (string of "0" and "1" for each output)
         order_from: [[str,str], ...]:    
                     obsolete & unused, historically linked to market.cpp/market.h
         time_received_is_tx_time: bool
             true if we sent the transaction. 
             seems to be used hitorically with sumbitorder/checkorde. 
         time_received: int
             time of the transaction.
         from_me: bool  
             true if we sent the transaction
         spent: bool: true if any of mapvalue.spent is spent
                      obsolete, use mapvalue.spent.
             
 """       
class WalletTx():
    def __init__(self, merkle_tx, merkle_tx_prev, map_value, order_from, time_received_is_tx_time, time_received, from_me, spent):
        self.merkle_tx = merkle_tx
        self.merkle_tx_prev = merkle_tx_prev
        self.map_value = map_value
        self.order_from = order_from
        self.time_received_is_tx_time = time_received_is_tx_time
        self.time_received = time_received
        self.from_me = from_me
        self.spent = spent
        
        self.outputs_spent = [False for _ in range(self.merkle_tx.tx.output_count())]
        if ("spent" in self.map_value):
            for index, c in enumerate(self.map_value["spent"]):
                self.outputs_spent[index] = (c != "0")

    def is_spent(self, n):
        return (self.outputs_spent[n])
    
    def __str__(self):
        return ("WalletTx(\n"  \
                "   merkle_tx:%s\n"  \
                "   merkle_tx_prev:%s\n"   \
                "   map_value:%s\n"   \
                "   order_from:%s\n"   \
                "   time_received_is_tx_time:%s,time_received:%s,from_me:%s,spent:%s\n"  \
                 % (str(self.merkle_tx), 
                    ",".join([str(m) for m in self.merkle_tx_prev]), 
                    str(self.map_value),
                    str(self.order_from),
                    self.time_received_is_tx_time,
                    time.strftime("%Y-%m-%d %H:%m:%S", time.gmtime(self.time_received)),
                    self.from_me,
                    self.spent,
                    ))
    