from itertools import ifilter, groupby
from collections import namedtuple
import collections

CHUNK_SIZE=16

"""
class ChunkHandle():
    def __init__(self, file_handle, header, chunkoffset):
        self.file_handle = file_handle
        self.header = header
        self.chunkoffset = chunkoffset
        
    def read(self, pos, length):
        pass

    def write(self, pos, data, fix_crc=True):
        pass
"""  
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

class CorruptLogIndexException(Exception):
    pass

class LogIndex(object):
    def __init__(self, logindexreader):
        self.reader = logindexreader
        
    def itercommits(self):
        for idx in self.logindexreader.iterentries():
            if idx.needs_commit:
                yield idx
 
    def iterchanges(self):
        for idx in self.logindexreader.iterentries():
            if idx.needs_commit:
                yield idx
 
    def get_last_opentx(self):
        pos = None
        for i, logindex in enumerate(self.reader.iterentries()):
            if logindex.command == LogIndexEntry.BEGIN_TX:
                pos = i
            if logindex.command == LogIndexEntry.END_TX:
                pos = None
        return pos

def commits(logindexentries):
    return ifilter(lambda e: e.needs_commit, logindexentries)

ATOMIC, TX, INCOMPLETE_TX = LOGINDEX_GROUPS = range(3)
LogGroup = collections.namedtuple("LogIndexGroup", "type changes")

def logindex_parse_groups(commands):
    """Parse transactions Groups. 

       Return (groups, incomplete) where:
            groups(list of list of int): list of indexes for each transactions
            incomplete(list of int): If non empty, the last incomplete transaction.
            
        >>> logindex_parse_groups([BEGIN_TX, WRITE, END_TX, BEGIN_TX, END_TX, WRITE, WRITE, BEGIN_TX, WRITE)
        ([[0,1,2],[3,4],[5],[6]], [7,8])
    """
    result = []
    intx, group = False, []
    for idx, cmd in enumerate(commands):
        group.append(idx)
        if cmd == LogIndexEntry.BEGIN_TX:
            if intx:
                raise CorruptLogIndexException("BEGIN_TX: TX already open")
            intx = True
        elif cmd == LogIndexEntry.END_TX:
            if not intx:
                raise CorruptLogIndexException("END_TX: no TX open")
            result.append(group)
            group = []
            intx = False
        elif not intx:
            result.append(group)
            group = []
    return (result, group)

def needscommit_are_coherent(logindex_entries):
    grouped = list(groupby([e.needs_commit for e in logindex_entries]))
    if len(grouped) > 3:
        return False
    if len(grouped) == 3:
        return not grouped[0][0]
    return True

def recover_logindex(logindex_reader):
    entries = logindex_reader.iterentries()
    if not needscommit_are_coherent(entries):
        raise CorruptLogIndexException("needs_commit fields are incoherent") 
    logidx_tocommit = [(logidx, idx) for idx, logidx in enumerate(entries) if logidx.needs_commit]
    _groups, incomplete_tx = logindex_parse_groups(logidx.command for logidx, idx in logidx_tocommit)
    for idx in reversed(incomplete_tx):
        pos = logidx_tocommit[idx][1]
        e = entries[pos]
        e.needs_commit = False
        logindex_reader.write_entry(pos, e)

class TxLog(object):
    def __init__(self, logindex_reader, logbuffer):
        self.logindex_reader = logindex_reader
        self.logbuffer = logbuffer
    def recover(self):
        recover_logindex(self.logindex_reader)

class TxChunkFile(object):
    def __init__(self, io, log):
        self.io = io
        self.log = log
    
    def recover(self):
        """ Verify logindex and erase last indexed transaction if incomplete """
        self.log.recover()

    def commit(self):
        pass
    
    def start_transaction(self):
        #TODO: remove assumption that it always writes at pos=0
        self.logindex.write_entry(0, LogIndexEntry(LogIndexEntry.BEGIN_TX))

    
    def write(self, address, data):
        logpos = self.logindex.allocate_buffer(len(data))
        self.logbuffer.write(logpos, address, data)
    
    
    
        
