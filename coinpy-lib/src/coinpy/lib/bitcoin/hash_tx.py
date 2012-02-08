# -*- coding:utf-8 -*-
"""
Created on 17 Nov 2011

@author: kris
"""
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer
from coinpy.model.protocol.structures.uint256 import uint256

TX_SERIALIZE = TxSerializer()

def hash_tx(tx):
    return (uint256.from_bytestr(doublesha256(TX_SERIALIZE.encode(tx))))

