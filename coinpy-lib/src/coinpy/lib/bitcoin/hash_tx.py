# -*- coding:utf-8 -*-
"""
Created on 17 Nov 2011

@author: kris
"""
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer
from coinpy.model.protocol.structures.uint256 import Uint256

TX_SERIALIZE = TxSerializer()

def hash_tx(tx):
    if tx.hash:
        return tx.hash
    if not tx.rawdata:
        tx.rawdata = TX_SERIALIZE.serialize(tx)
    tx.hash = Uint256.from_bytestr(doublesha256(tx.rawdata))
    return tx.hash

