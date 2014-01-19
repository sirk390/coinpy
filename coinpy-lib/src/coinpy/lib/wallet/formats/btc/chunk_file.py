from itertools import ifilter, groupby
from collections import namedtuple
import collections
from coinpy.lib.wallet.formats.btc.serialization import ChunkHeaderSerializer
import zlib
from coinpy.tools.functools import only
from coinpy.lib.wallet.formats.btc.file_handle import IoSectionHandle
from io import SEEK_END
import StringIO

CHUNK_SIZE=16

from coinpy.lib.wallet.formats.btc.file_model import LogIndexEntry, ChunkHeader

class ChunkHeaderReader(object):
    """ Go through a file, read and deserialize ChunkHeader's """
    def __init__(self, iosize):
        self.iosize = iosize
        
    @staticmethod
    def read(io, pos):
        """ Read and returm a ChunkHeader from the position `pos` in the file 
            Returns None if the file is too short.
        """ 
        data = io.read(pos, ChunkHeaderSerializer.SERIALIZED_LENGTH)
        return ChunkHeaderSerializer.deserialize(data)

    @staticmethod
    def readall(io, iosize, start_pos):
        pos = start_pos
        while pos <= iosize - ChunkHeaderSerializer.SERIALIZED_LENGTH:
            chunk_header = ChunkHeaderReader.read(io, pos)
            yield pos, chunk_header
            pos += ChunkHeaderSerializer.SERIALIZED_LENGTH + chunk_header.length

    def write(self):
        pass
    
class ChunkIO(object):
    """ Read and write to a single chunk of a file """
    def __init__(self, chunkfile, chunkid, size):
        self.chunkfile = chunkfile
        self.chunkid = chunkid
        self.size = size
        
    def write(self, offset, data):
        self.chunkfile.write(self.chunkid, offset, data)
        
    def read(self, offset, length):
        return self.chunkfile.read(self.chunkid, offset, length)
    
    @classmethod
    def from_name(cls, chunk_file, name):
        pos, header = chunk_file.get_chunk(name)
        return cls(chunk_file, pos, header.length)
    
class ChunkFile(object):
    """ 
        chunk_reader (instance of ChunkReader)
        chunkinfos ( dict {int => ChunkHeader}: Dictionary mapping from IO index to ChunkHeader
    """
    def __init__(self, io, chunkheaders=None, serializer=ChunkHeaderSerializer):
        self.io = io
        self.chunkheaders = chunkheaders or {}
        self.serializer = serializer
        
    def get_chunk(self, name):
        """ Get the position of chunk called {name} 
            Raises an exception if not found, or if there are more than one"""
        pos_header = [(pos, header) for pos, header in self.chunkheaders.iteritems() if header.name == name]
        return only(pos_header)

    def write(self, chunkpos, address, data):
        header = self.chunkheaders[chunkpos]
        if not (0 <= address <= header.length - len(data)): 
            raise Exception("write: out of chunk range")
        self.io.write(self._chunk_start(chunkpos) + address, data)
        self._fix_crc(chunkpos)
        
    def _fix_crc(self, chunkpos):
        header = self.chunkheaders[chunkpos]
        data = self.io.read(self._chunk_start(chunkpos),header.length)
        header.crc = zlib.crc32(data)
        self.io.write(chunkpos,  self.serializer.serialize(header))

    def read(self, chunkpos, address, length):
        header = self.chunkheaders[chunkpos]
        if not (0 <= address <= header.length - length): 
            raise Exception("read: out of chunk range")
        return self.io.read(self._chunk_start(chunkpos) + address, length)
    
    def _chunk_start(self, chunkpos):
        return chunkpos + self.serializer.SERIALIZED_LENGTH
    
    @staticmethod
    def new(self, chunkdefs):
        """
            chunkdefs (list of tuple (name, version, contents) )
        """
        pass
    
    def append_chunk(self, name, length, version=1):
        data = "\x00" * length
        header = ChunkHeader(name=name, version=version, length=length, crc=zlib.crc32(data))
        headerdata = self.serializer.serialize(header)
        self.io.seek(0, SEEK_END)
        pos = self.io.tell()
        self.io.write(data=headerdata + data)
        self.chunkheaders[pos] = header
        return pos

    @staticmethod
    def open(io, iosize):
        start_pos = io.tell()
        chunkheaders = dict( (pos, header) for pos, header in ChunkHeaderReader.readall(io, iosize, start_pos))
        return ChunkFile(io, chunkheaders)


class MultiChunkIO(object):
    """ Write to multiple chunks using a StringIO """ 
    def __init__(self, ios):
        self.ios = ios
        
    def write(self, chunkpos, address, data):
        self.ios[chunkpos].seek(address)
        return self.ios[chunkpos].write(data)
        
    def read(self, chunkpos, address, length):
        self.ios[chunkpos].seek(address)
        return self.ios[chunkpos].read(length)
    
    @classmethod
    def using_stringios(cls, pos_sizes):
        ios = dict((pos, StringIO.StringIO("\x00" * size)) for pos, size in pos_sizes.iteritems() )
        return cls(ios)

