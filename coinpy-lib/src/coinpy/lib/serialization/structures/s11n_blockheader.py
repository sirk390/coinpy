# -*- coding:utf-8 -*-
"""
Created on 6 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.structures.s11n_uint256 import Uint256Serializer
from coinpy.model.protocol.structures.blockheader import BlockHeader
from coinpy.lib.serialization.common.serializer import Serializer


class BlockheaderSerializer(Serializer):
    def __init__(self, flags=0):
        self.BLOCKHEADER = Structure([Field("<I", "version"),
                                      Uint256Serializer("hash_prev"),
                                      Uint256Serializer("hash_merkle"),
                                      Field("<I", "time"),
                                      Field("<I", "bits"),
                                      Field("<I", "nonce")], "txindex")

    def get_size(self, blockheader):
        return (self.BLOCKHEADER.get_size([blockheader.version,
                                           blockheader.hash_prev,
                                           blockheader.hash_merkle,
                                           blockheader.time,
                                           blockheader.bits,
                                           blockheader.nonce]))

    def serialize(self, blockheader):
        return (self.BLOCKHEADER.serialize([blockheader.version,
                                            blockheader.hash_prev,
                                            blockheader.hash_merkle,
                                            blockheader.time,
                                            blockheader.bits,
                                            blockheader.nonce]))

    def deserialize(self, data, cursor=0):
        (version, hash_prev, hash_merkle, time, bits, nonce), cursor = self.BLOCKHEADER.deserialize(data, cursor)
        return (BlockHeader(version, hash_prev, hash_merkle, time, bits, nonce), cursor)

        