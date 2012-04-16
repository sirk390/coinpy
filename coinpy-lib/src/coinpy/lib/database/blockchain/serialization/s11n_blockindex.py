# -*- coding:utf-8 -*-
"""
Created on 5 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field

from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.lib.database.blockchain.objects.blockindex import DbBlockIndex


class BlockIndexSerializer():
    BLOCKINDEX = Structure([Field("<I", "version"),
                            Uint256Serializer("hash_next"),
                            Field("<I", "file"),
                            Field("<I", "blockpos"),
                            Field("<I", "height"),
                            BlockheaderSerializer()], "txindex")
    
    def __init__(self):
        pass
        
    def serialize(self, blockindex_obj):
        return (self.BLOCKINDEX.serialize([blockindex_obj.version,
                                           blockindex_obj.hash_next,
                                           blockindex_obj.file,
                                           blockindex_obj.blockpos,
                                           blockindex_obj.height,
                                           blockindex_obj.blockheader]))

    def deserialize(self, data, cursor=0):
        result, cursor = self.BLOCKINDEX.deserialize(data, cursor)
        (version, hash_next, file, blockpos, height, blockheader) = result
        return (DbBlockIndex(version, hash_next, file, blockpos, height, blockheader), cursor)

        