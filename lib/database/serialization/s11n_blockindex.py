# -*- coding:utf-8 -*-
"""
Created on 5 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field

from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.serialization.structures.s11n_uint256 import uint256_encoder
from coinpy.lib.serialization.structures.s11n_blockheader import blockheader_serializer
from coinpy.lib.database.objects.blockindex import DbBlockIndex


class BlockIndexSerializer():
    BLOCKINDEX = Structure([Field("<I", "version"),
                            uint256_encoder("hash_next"),
                            Field("<I", "file"),
                            Field("<I", "blockpos"),
                            Field("<I", "height"),
                            blockheader_serializer()], "txindex")
    
    def __init__(self):
        pass
        
    def encode(self, blockindex_obj):
        return (self.BLOCKINDEX.encode(blockindex_obj.version,
                                       blockindex_obj.hash_next,
                                       blockindex_obj.file,
                                       blockindex_obj.blockpos,
                                       blockindex_obj.height,
                                       blockindex_obj.blockheader))

    def decode(self, data, cursor=0):
        result, cursor = self.BLOCKINDEX.decode(data, cursor)
        (version, hash_next, file, blockpos, height, blockheader) = result
        return (DbBlockIndex(version, hash_next, file, blockpos, height, blockheader), cursor)

        