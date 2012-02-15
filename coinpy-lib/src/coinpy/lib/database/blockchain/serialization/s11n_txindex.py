# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.database.blockchain.serialization.s11n_disktxpos import DiskTxPosSerializer
from coinpy.lib.database.blockchain.objects.txindex import DbTxIndex



class TxIndexSerializer():
    TXINDEX = Structure([Field("<I", "version"),
                         DiskTxPosSerializer(),
                         VarsizelistSerializer( VarintSerializer(), DiskTxPosSerializer() )], "txindex")

    def __init__(self):
        pass

    def serialize(self, txindex_obj):
        return (self.TXINDEX.serialize([txindex_obj.version,
                                        txindex_obj.pos,
                                        txindex_obj.spent]))

    def deserialize(self, data, cursor=0):
        (version, pos, spent), cursor = self.TXINDEX.deserialize(data, cursor)
        return (DbTxIndex(version, pos, spent), cursor)

