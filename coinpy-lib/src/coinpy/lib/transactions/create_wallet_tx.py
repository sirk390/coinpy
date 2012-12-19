from coinpy.lib.transactions.merkle_tree import get_merkle_branch
from coinpy.model.protocol.structures.merkle_tx import MerkleTx
from coinpy.model.protocol.structures.wallet_tx import WalletTx
from coinpy.lib.transactions.hash_tx import hash_tx
import time

COPY_DEPTH = 1

#see wallet.cpp:580/AddSupportingTransactions
def create_wallet_tx(blockchain, merkle_tx, txtime):
    input_txs = [merkle_tx]
    merkle_tx_prev = {}
    #Fixed version of AddSupportingTransactions
    """
    for d in range(COPY_DEPTH):
        next_input_txs = []
        for tx in input_txs:
            for txin in tx.tx.in_list:
                tx_handle = blockchain.get_transaction_handle(txin.previous_output.hash)
                tx = tx_handle.get_transaction()
                block_handle = tx_handle.get_block()
                merkle_tx = MerkleTx(tx_handle.get_transaction(), 
                                     block_handle.hash, 
                                     get_merkle_branch(block_handle.get_block(), txin.previous_output.index), 
                                     txin.previous_output.index)
                merkle_tx_prev[hash_tx(tx)] = merkle_tx #put in a map for unicity of hashes
                next_input_txs.append(merkle_tx_prev)
    """
    return WalletTx(merkle_tx, 
                    merkle_tx_prev.values(),
                    {"spent": "0" * len(merkle_tx.tx.out_list)},
                    [],
                    True,
                    txtime,
                    True,
                    False)
    
if __name__ == '__main__':
    pass
