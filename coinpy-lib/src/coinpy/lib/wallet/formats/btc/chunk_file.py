from itertools import ifilter, groupby
from collections import namedtuple
import collections

CHUNK_SIZE=16

from coinpy.lib.wallet.formats.btc.file_model import LogIndexEntry

class ChunkFile(object):
    def __init__(self, filename, fileio_api):
        self.filename = filename
        self.fileio_api = fileio_api
        self.chunk_handles = []        
        
    def open(self):
        self.handle = self.fileio_api.open(self.filename, "wb")
        self.loadchunks()
        
    def create(self):
        self.handle = self.fileio_api.open(self.filename, "wb")
    
    def open_or_create(self):
        if not self.fileio_api.exists(self.filename):
            return self.create()
        return self.open()
    
            
    def read(self, chunk, pos, length):
        return self.chunk_handles[pos].read(length)

    def write(self, chunk, pos, data):
        return self.chunk_handles[pos].write(data)
    
    def appendchunk(self):
        pass
    
    def iterchunks(self):
        for c in self.chunk_handles:
            yield c
