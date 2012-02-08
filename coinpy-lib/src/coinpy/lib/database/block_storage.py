# -*- coding:utf-8 -*-
"""
Created on 6 Aug 2011

@author: kris
"""
import os
from coinpy.lib.serialization.exceptions import MissingDataException
from coinpy.lib.serialization.magic import MAGICS
import struct
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.lib.serialization.structures.s11n_block import BlockSerializer
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer

BLOCKHEADER_READSIZE=1024
BLOCK_READSIZE=8*1024
TX_READSIZE=8*1024

class BlockStorage:
    def __init__(self, runmode, directory):
        self.runmode = runmode
        self.directory = directory
        self.openhandles = {}
        self.blockheaderserialize =  BlockheaderSerializer()
        self.blockserialize =  BlockSerializer()
        self.txserialize = TxSerializer()
        
    def saveblock(self, block):
        file = 1
        handle = self._gethandle(file)
        handle.seek(0, os.SEEK_END)
        blockdata = self.blockserialize.serialize(block)
        #Write index header
        handle.write(struct.pack("<I", MAGICS[self.runmode]))
        handle.write(struct.pack("<I", len(blockdata)))
        blockpos = handle.tell()
        #Write block
        handle.write(blockdata)
        #Flush and commit to disk
        
        #FIXME?
        #handle.flush()
        #os.fsync(handle.fileno())
        return (file, blockpos)
       
    def _gethandle(self, filenum):
        if file not in self.openhandles:
            filename = os.path.join(self.directory, "blk%04d.dat" % (filenum))
            handle = open(filename, "a+b")
            self.openhandles[file] = handle
            return (handle)
        return self.openhandles[file]
    
    def _read_data(self, handle, size):
        data = handle.read(size)
        if len(data) == 0:
            raise Exception("End of file") 
        return data
        
    def load_blockheader(self, filenum, blockpos):
        handle = self._gethandle(filenum)
        handle.seek(blockpos)
        block, data = None, self._read_data(handle, BLOCKHEADER_READSIZE)
        while (block is None):
            try:
                block, _ = self.blockheaderserialize.deserialize(data, 0)
            except MissingDataException:
                #FIXME: infinite loop when end of file
                data += self._read_data(handle, BLOCKHEADER_READSIZE)
        return (block)
    
    def load_block(self, filenum, blockpos):
        handle = self._gethandle(filenum)
        handle.seek(blockpos)
        block, data = None, self._read_data(handle, BLOCK_READSIZE)
        while (block is None):
            try:
                block, _ = self.blockserialize.deserialize(data, 0)
            except MissingDataException:
                data += self._read_data(handle, BLOCK_READSIZE)
        return (block)
    
    def load_tx(self, filenum, txpos):
        handle = self._gethandle(filenum)
        handle.seek(txpos)
        tx, data = None, self._read_data(handle, TX_READSIZE)
        while (tx is None):
            try:
                tx, _ = self.txserialize.deserialize(data, 0)
            except MissingDataException:
                data += self._read_data(handle, TX_READSIZE)
        return (tx)
