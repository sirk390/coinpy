# -*- coding:utf-8 -*-
"""
Created on 8 Aug 2011

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_blockheader import blockheader_serializer
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.lib.serialization.structures.s11n_tx import tx_encoder

BLOCK_SERIALIZE = blockheader_serializer()
TX_SERIALIZE = tx_encoder()
    
def hashblock(block):
    return (uint256.from_bytestr(doublesha256(BLOCK_SERIALIZE.encode(block.blockheader))))

def hashtx(tx):
    return (uint256.from_bytestr(doublesha256(TX_SERIALIZE.encode(tx))))




if __name__ == '__main__':
    from coinpy.model.genesis import GENESIS

    print hashblock(GENESIS)
    #000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
