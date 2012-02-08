# -*- coding:utf-8 -*-
"""
Created on 10 Jan 2012

@author: kris
"""
from coinpy.tools.bitcoin.sha256 import double_sha256_2_input
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.model.protocol.structures.uint256 import uint256

"""
    hashes: list of byte string hashes ( use uint256.to_bytestr() )
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
        

def compute_merkle_root(block):
    hashes = [hash_tx(tx).to_bytestr() for tx in block.transactions]
    while (len(hashes) != 1):
        hashes = next_merkle_level(hashes)

    return (uint256.from_bytestr(hashes[0]))
    
    