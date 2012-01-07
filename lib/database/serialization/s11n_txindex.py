# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.structures.s11n_varint import varint_encoder
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.database.serialization.s11n_disktxpos import DiskTxPosSerializer
from coinpy.lib.database.objects.txindex import DbTxIndex



class TxIndexSerializer():
    TXINDEX = Structure([Field("<I", "version"),
                         DiskTxPosSerializer(),
                         varsizelist_encoder( varint_encoder(), DiskTxPosSerializer() )], "txindex")

    def __init__(self):
        pass

    def encode(self, txindex_obj):
        return (self.TXINDEX.encode(txindex_obj.version,
                               txindex_obj.pos,
                               txindex_obj.spent))

    def decode(self, data, cursor=0):
        (version, pos, spent), cursor = self.TXINDEX.decode(data, cursor)
        return (DbTxIndex(version, pos, spent), cursor)

