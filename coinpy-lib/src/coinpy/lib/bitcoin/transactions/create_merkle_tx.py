from coinpy.lib.bitcoin.merkle_tree import get_merkle_branch
from coinpy.model.protocol.structures.merkle_tx import MerkleTx

def create_merkle_tx(blockhash, block, index_tx):
    return MerkleTx(block.transactions[index_tx], 
                    blockhash, 
                    get_merkle_branch(block, index_tx), 
                    index_tx)

if __name__ == '__main__':
    pass
