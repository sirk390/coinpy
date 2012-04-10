# -*- coding:utf-8 -*-
"""
Created on 10 Jan 2012

@author: kris
"""
from coinpy.tools.bitcoin.sha256 import double_sha256_2_input
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.model.protocol.structures.uint256 import uint256

"""
    hashes: list of bytestring hashes ( use uint256.get_bytestr() )
"""
def next_merkle_level(hashes):
    n = len(hashes)
    result = []
    # if odd number of hashes, dupplicate the last one.
    if n % 2:
        hashes.append(hashes[-1])
        n += 1
    # compute the next level of hashes
    for i in range(n/2):
        result.append(double_sha256_2_input(hashes[i*2], hashes[i*2+1]))
    return (result)

    
def get_merkle_tree(block):
    merkle_tree = []
    merkle_tree.append([hash_tx(tx).get_bytestr() for tx in block.transactions])
    while (len(merkle_tree[-1]) != 1):
        merkle_tree.append(next_merkle_level(merkle_tree[-1]))
    return (merkle_tree)

"""Get the merkle branch of a transaction.

block:    block that contains the transaction
index_tx: index of the transaction in the block

Return value: [list of uint256] 
The first element is a hash of a transaction at the bottom of the merkle tree.  
The last element is the merkle root.

The algorithm uses XOR 1, to select the opposite element at each level.
"""
def get_merkle_branch(block, index_tx):
    merkle_branch = []
    merkle_tree = get_merkle_tree(block)
    for level in merkle_tree:
        merkle_branch.append(uint256.from_bytestr(level[min(index_tx^1, len(level)-1)]))
        index_tx = index_tx >> 1
    return (merkle_branch)

"""
static uint256 CheckMerkleBranch(uint256 hash, const vector<uint256>& vMerkleBranch, int nIndex)
    {
        if (nIndex == -1)
            return 0;
        foreach(const uint256& otherside, vMerkleBranch)
        {
            if (nIndex & 1)
                hash = Hash(BEGIN(otherside), END(otherside), BEGIN(hash), END(hash));
            else
                hash = Hash(BEGIN(hash), END(hash), BEGIN(otherside), END(otherside));
            nIndex >>= 1;
        }
        return hash;
    }

"""


def compute_merkle_root(block):
    hashes = [hash_tx(tx).get_bytestr() for tx in block.transactions]
    while (len(hashes) != 1):
        hashes = next_merkle_level(hashes)
    return (uint256.from_bytestr(hashes[0]))


