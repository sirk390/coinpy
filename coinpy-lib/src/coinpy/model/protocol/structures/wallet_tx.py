import time

class WalletTx():
    """
         WalletTx:    A transaction with metadata as saved in the wallet
             merkle_tx: (MerkleTx) the transaction 
             merkle_tx_prev: (MerkleTx) of the supporting the transactions.
                             Contains the merkle_tx for each input transaction, and input transaction 
                             of these transactions, etc... until COPY_DEPTH (=3)
             map_value: {key => value} map for saving metadata information.
                         recognized keys: 
                             "fromaccount", account name for JSON-RPC, default=empty
                             "spent" (string of "0" and "1" for each output) (probably only usefull for outputs that are mine) 
             order_from: [[str,str], ...]:    
                         obsolete & unused, historically linked to market.cpp/market.h
                         use []
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
    def __init__(self, 
                 merkle_tx, merkle_tx_prev, map_value, order_from,
                 time_received_is_tx_time, time_received, from_me, spent):
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
    
    def set_spent(self, n):
        self.outputs_spent[n] = True
        spent = "".join({False:"0", True:"1"}[s] for s in self.outputs_spent)
        self.map_value["spent"] = spent

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
    