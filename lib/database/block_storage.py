# -*- coding:utf-8 -*-
"""
Created on 6 Aug 2011

@author: kris
"""
from coinpy.model.protocol.structures.block import Block
from coinpy.lib.serialization.messages.s11n_block import block_encoder
from coinpy.model.protocol.structures.tx import tx
from coinpy.lib.serialization.messages.s11n_tx import tx_encoder
import os
from coinpy.lib.serialization.exceptions import MissingDataException
from coinpy.lib.serialization.magic import MAGICS
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.common.varsizelist import varsizelist_encoder
import struct

BLOCK_READSIZE=1024*1024
TX_READSIZE=1024*16

class BlockStorage:
    def __init__(self, runmode, directory):
        self.runmode = runmode
        self.directory = directory
        self.openhandles = {}
        self.blockserialize =  block_encoder()
        self.txserialize = tx_encoder()
        
    def saveblock(self, block):
        file = 1
        handle = self._gethandle(file)
        handle.seek(0, os.SEEK_END)
        blockdata = self.blockserialize.encode(block)
        #Write index header
        handle.write(struct.pack("<I", MAGICS[self.runmode]))
        handle.write(struct.pack("<I", len(blockdata)))
        blockpos = handle.tell()
        #Write block
        handle.write(blockdata)
        #Flush and commit to disk
        handle.flush()
        os.fsync(handle.fileno())
        return (file, blockpos)
       
    def _gethandle(self, filenum):
        if file not in self.openhandles:
            filename = os.path.join(self.directory, "blk%04d.dat" % (filenum))
            handle = open(filename, "a+b")
            self.openhandles[file] = handle
            return (handle)
        return self.openhandles[file]

    def load_block(self, filenum, blockpos):
        handle = self._gethandle(filenum)
        handle.seek(blockpos)
        block, data = None, handle.read(BLOCK_READSIZE)
        while (block is None):
            try:
                block, _ = self.blockserialize.decode(data, 0)
            except MissingDataException:
                data += handle.read(BLOCK_READSIZE)
        return (block)
    
    def load_tx(self, filenum, txpos):
        handle = self._gethandle(filenum)
        handle.seek(txpos)
        tx, data = None, handle.read(TX_READSIZE)
        while (tx is None):
            try:
                tx, _ = self.txserialize.decode(data, 0)
            except MissingDataException:
                data += handle.read(TX_READSIZE)
        return (tx)

