# -*- coding:utf-8 -*-
"""
Created on 6 Jul 2011

@author: kris
"""
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.lib.serialization.structures.s11n_uint256 import uint256_encoder
from coinpy.model.protocol.structures.blockheader import BlockHeader


class blockheader_serializer():
    def __init__(self, flags=0):
        self.BLOCKHEADER = Structure([Field("<I", "version"),
                                      uint256_encoder("hash_prev"),
                                      uint256_encoder("hash_merkle"),
                                      Field("<I", "time"),
                                      Field("<I", "bits"),
                                      Field("<I", "nonce")], "txindex")

    def get_size(self, blockheader):
        return (self.BLOCKHEADER.get_size(blockheader.version,
                                          blockheader.hash_prev,
                                          blockheader.hash_merkle,
                                          blockheader.time,
                                          blockheader.bits,
                                          blockheader.nonce))

    def encode(self, blockheader):
        return (self.BLOCKHEADER.encode(blockheader.version,
                                        blockheader.hash_prev,
                                        blockheader.hash_merkle,
                                        blockheader.time,
                                        blockheader.bits,
                                        blockheader.nonce))

    def decode(self, data, cursor=0):
        (version, hash_prev, hash_merkle, time, bits, nonce), cursor = self.BLOCKHEADER.decode(data, cursor)
        return (BlockHeader(version, hash_prev, hash_merkle, time, bits, nonce), cursor)

        