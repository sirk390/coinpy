# -*- coding:utf-8 -*-
"""
Created on 25 Jun 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.database.objects.disktxpos import DiskTxPos

class DiskTxPosSerializer():
    DISKTXPOS = Structure([Field("<I", "file"),
                           Field("<I", "blockpos"),
                           Field("<I", "txpos")], "disktxpos")

    def encode(self, disktxpos_obj):
        return (self.DISKTXPOS.encode(disktxpos_obj.file,
                                      disktxpos_obj.blockpos,
                                      disktxpos_obj.txpos))

    def decode(self, data, cursor=0):
        (file, nblockpos, ntxpos), cursor = self.DISKTXPOS.decode(data, cursor)
        return (DiskTxPos(file, nblockpos, ntxpos), cursor)
