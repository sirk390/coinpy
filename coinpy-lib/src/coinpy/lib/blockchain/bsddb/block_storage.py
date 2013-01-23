import os
from coinpy.lib.serialization.exceptions import MissingDataException
from coinpy.lib.serialization.magic import MAGICS
import struct
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.lib.serialization.structures.s11n_block import BlockSerializer
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer

BLOCKHEADER_READSIZE=1024
BLOCK_READSIZE=1024*1024
TX_READSIZE=8*1024

class StorageFile():
    def __init__(self, directory, filenum):
        file.__init__()
        self._directory = directory
        self._filename = os.path.join(self._directory, "blk%04d.dat" % (filenum))
        self.handle = open(self.filename, "a+b")
    
class BlockStorage(object):
    """Storage consisting in a pool of "blk{NNNN}.dat" files where {NNNN} is the integer "filenum".
       
       The files contain serialized blocks with an extra header. 
       A block can be located by its filenum and fileoffset.
    
       Limitation: Currently it writes only a single filenum(1).
    """
    def __init__(self, 
                 runmode, 
                 directory,
                 storagefiles={}, 
                 blockheaderserialize=BlockheaderSerializer(),
                 blockserialize=BlockSerializer(),
                 txserialize=TxSerializer(),
                 blockheader_readsize=BLOCKHEADER_READSIZE,
                 block_readsize=BLOCK_READSIZE,
                 tx_readsize=TX_READSIZE):
        self.runmode = runmode
        self.directory = directory
        self.storagefiles = storagefiles
        self.blockheaderserialize = blockheaderserialize
        self.blockserialize = blockserialize
        self.txserialize = txserialize
        self.blockheader_readsize = blockheader_readsize
        self.block_readsize = block_readsize
        self.tx_readsize = tx_readsize
        
    def saveblock(self, block):
        file = 1
        handle = self._gethandle(file)
        handle.seek(0, os.SEEK_END)
        if not block.rawdata:
            block.rawdata = self.blockserialize.serialize(block)
        #Write index header
        handle.write(struct.pack("<I", MAGICS[self.runmode]))
        handle.write(struct.pack("<I", len(block.rawdata)))
        blockpos = handle.tell()
        #Write block
        handle.write(block.rawdata)
        #Flush and commit to disk
        handle.flush()
        os.fsync(handle.fileno())
        return (file, blockpos)
    
    def commit(self):
        for filenum, file in self.storagefiles.iteritems():
            file.handle.flush()
            os.fsync(file.handle.fileno())
        
    def _gethandle(self, filenum):
        if filenum not in self.storagefiles:
            self.storagefiles[filenum] = StorageFile(self.directory, filenum)
        return self.storagefiles[filenum].handle
    
    def _read_data(self, handle, size):
        data = handle.read(size)
        if len(data) == 0:
            raise Exception("End of file") 
        return data

    def load_serialized_data(self, filenum, pos, serializer, readsize):
        handle = self._gethandle(filenum)
        handle.seek(pos)
        block, data = None, self._read_data(handle, readsize)
        while (block is None):
            try:
                block, _ = serializer.deserialize(data, 0)
            except MissingDataException:
                data += self._read_data(handle, readsize)
        return (block)
        
    def load_blockheader(self, filenum, blockpos):
        return self.load_serialized_data(filenum, blockpos, self.blockheaderserialize, self.blockheader_readsize)
    
    def load_block(self, filenum, blockpos):
        return self.load_serialized_data(filenum, blockpos, self.blockserialize, self.block_readsize)
    
    def load_tx(self, filenum, txpos):
        return self.load_serialized_data(filenum, txpos, self.txserialize, self.tx_readsize)


