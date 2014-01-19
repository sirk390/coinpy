from itertools import ifilter, groupby
from collections import namedtuple
import collections
from pydoc import deque
from coinpy.tools.event import Event
from coinpy.tools.functools import rindex, lindex
from coinpy.lib.wallet.formats.btc.serialization import LogIndexEntrySerializer
from coinpy.lib.wallet.formats.btc.entry_reader import FixedSizeEntryReader,\
    LogIndexReader, LogBufferReader
from coinpy.lib.wallet.formats.btc.chunk_file import ChunkFile, ChunkIO

CHUNK_SIZE=16

from coinpy.lib.wallet.formats.btc.file_model import LogIndexEntry, Log,\
    LogHeader, LOG_INDEX_NAME, LOG_BUFFER_NAME

class CorruptLogIndexException(Exception):
    pass


class LogIndex(object):
    """
    Attributes:
        tocommit (collections.deque)
    """
    def __init__(self, tocommit=None):
        self.tocommit = tocommit or deque()
        self.ON_COMMITING = Event()
        self.ON_LOG = Event()
        self.ON_REVERTLOG = Event()
        self.ON_COMMITED = Event()
        
    def commit_step(self):
        assert self.tocommit
        logidx = self.tocommit.popleft()
        if logidx.command == LogIndexEntry.WRITE:
            self.ON_COMMITING.fire(logindex=logidx)
        logidx.needs_commit = False    
        self.ON_COMMITED.fire(logindex=logidx)

    def commit(self):
        while self.tocommit:
            self.commit_step()

    def log(self, logindex):
        logindex.needs_commit = True
        self.tocommit.append(logindex)
        self.ON_LOG.fire(logindex=logindex)

    def revertlog(self):
        logidx = self.tocommit.pop()
        self.ON_REVERTLOG.fire(logindex=logidx)

    def recover(self):
        # Remove not entirely written logindex transactions at the end.
        idx = rindex(self.tocommit, lambda i: i.is_tx_command())
        if idx is not None and self.tocommit[idx].command == LogIndexEntry.BEGIN_TX:
            for i in range(len(self.tocommit) - idx):
                self.revertlog()
        # Commit at least the first transaction
        idx = lindex(self.tocommit, lambda i: i.is_tx_command())
        if idx is not None and self.tocommit[idx].command == LogIndexEntry.END_TX:
            for i in range(idx):
                self.commit_step()

class SerializedLogIndex(LogIndex):
    """
    Attributes:
        logindex_reader (instance of LogIndexReader)
        tocommit (collections.deque)
    """
    def __init__(self, logindex_reader, tocommit=None, start_pos=0):
        super(SerializedLogIndex, self).__init__(tocommit)
        self.logindex_reader = logindex_reader
        self.start_pos = start_pos
        self.ON_LOG.subscribe(self.on_log)
        self.ON_REVERTLOG.subscribe(self.on_revertlog)
        self.ON_COMMITED.subscribe(self.on_commited)

    def on_revertlog(self, event):
        self.logindex_reader.write_entry(self.start_pos+len(self.tocommit), event.logindex)

    def on_log(self, event):
        self.logindex_reader.write_entry(self.start_pos+len(self.tocommit)-1, event.logindex)

    def on_commited(self, event):
        self.logindex_reader.write_entry(self.start_pos, event.logindex)
        self.start_pos += 1
        if not self.tocommit:
            self.start_pos = 0

    @staticmethod
    def new(logindex_reader):
        for i in range(logindex_reader.nbentries):
            logindex_reader.write_entry(i, LogIndexEntry(LogIndexEntry.WRITE, needs_commit=False))
        return SerializedLogIndex(logindex_reader)
    
    #@staticmethod
    #def writenew(io, nbentries):
    #     for i in range(nbentries):
    #        io.write(offset=i * LogIndexEntrySerializer.SERIALIZED_LENGTH, 
    #                 data=LogIndexEntrySerializer.serialize(LogIndexEntry(LogIndexEntry.WRITE, needs_commit=False)))

    @staticmethod
    def load(logindex_reader):
        start_pos, end_pos = None, None
        entries = list(logindex_reader.iterentries())
        for i, idx in enumerate(entries):
            if idx.needs_commit:
                if start_pos is None:
                    start_pos = i
                elif end_pos is not None:
                    raise CorruptLogIndexException("needs_commit fields are incoherent")
            else:
                if start_pos is not None:
                    if end_pos is None:
                        end_pos = i
                #else just advance
        end_pos = end_pos if end_pos is not None else i 
        return SerializedLogIndex(logindex_reader, deque(entries[start_pos:end_pos]), start_pos=0)


class LogBuffer(object):
    def __init__(self, logbuffer_reader, writelogs=None):
        self.logbuffer_reader = logbuffer_reader
        self.writelogs = {} if writelogs is None else writelogs
        
    def getunallocated(self):
        #Can be improved a lot by keeping this in memory in a sorted structure
        last_end = 0
        unallocated = []
        for (start_pos, end_pos), log in sorted(self.writelogs.iteritems()):
            if last_end != start_pos:
                unallocated.append((last_end, start_pos))
            last_end = end_pos
        if last_end != self.logbuffer_reader.iosize:
            unallocated.append((last_end, self.logbuffer_reader.iosize))
        return unallocated
    
    def find_empty_location(self, sizeneeded):
        for start, end in self.getunallocated():
            if sizeneeded <= (end - start):
                return start
        raise Exception("LogBuffer Is Full")

    def find_empty_location_for_log(self, log_to_add):
        sizeneeded = self.logbuffer_reader.get_size(log_to_add)
        return self.find_empty_location(sizeneeded)

    @staticmethod
    def load(logindex, logbuffer_reader):
        writelist = filter(lambda idx: idx.is_write(), logindex.tocommit)
        writelogs = {}
        for write in writelist:
            log, size = logbuffer_reader.read_entry(write.argument)
            writelogs[(write.argument, write.argument+size)] = log
        return LogBuffer(logbuffer_reader, writelogs)
    
    def write_entry(self, pos, log):
        size = self.logbuffer_reader.write_entry(pos, log)
        self.writelogs[(pos, pos+size)] = log

    def read_entry(self, pos):
        log, length = self.logbuffer_reader.read_entry(pos)
        return log


class TransactionalChunkFile(object):
    def __init__(self, chunkfile, logindex, logbuffer, logindexpos, logbufferpos):
        self.chunkfile = chunkfile
        self.logindex = logindex
        self.logbuffer = logbuffer
        self.logindexpos = logindexpos
        self.logbufferpos = logbufferpos

        self.logindex.ON_COMMITING.subscribe(self.on_commiting)
        
    def recover(self):
        self.logindex.recover()

    def start_transaction(self):
        self.logindex.log(LogIndexEntry(LogIndexEntry.BEGIN_TX))

    def write(self, chunkid, address, data):
        size = len(data)
        log = Log(LogHeader(chunkid, address, len(data)), data, self.chunkfile.read(chunkid, address, size))
        bufferpos = self.logbuffer.find_empty_location_for_log(log)
        self.logbuffer.write_entry(bufferpos, log)
        self.logindex.log(LogIndexEntry(LogIndexEntry.WRITE, bufferpos))

    def read(self, chunkid, address, length):
        return self.chunkfile.read(chunkid, address, length)
    
    def end_transaction(self):
        self.logindex.log(LogIndexEntry(LogIndexEntry.END_TX))

    def on_commiting(self, event):
        """ Triggered when applying the write-ahead-log to disk by the LogIndex
        before the "needs_commit" is unset.
        If self.io.write raises an Exception, "need_commits" will be unchanged.
        """
        logidx = event.logindex
        log = self.logbuffer.read_entry(logidx.argument)
        self.chunkfile.write(log.logheader.chunk, log.logheader.address, log.data)
 
    def commit(self):
        self.logindex.commit()
    
    @classmethod
    def load(cls, io, iosize):
        chunkfile = ChunkFile.open(io, iosize)
        logindexio = ChunkIO.from_name(chunkfile, LOG_INDEX_NAME)
        logbufferio = ChunkIO.from_name(chunkfile, LOG_BUFFER_NAME)
       
        logindex_reader = LogIndexReader(logindexio, logindexio.size/LogIndexEntrySerializer.SERIALIZED_LENGTH)
        logindex = SerializedLogIndex.load(logindex_reader)

        logbuffer_reader = LogBufferReader(logbufferio, logbufferio.size)
        logbuffer = LogBuffer.load(logindex, logbuffer_reader)
                
        return cls(chunkfile, logindex, logbuffer, logindexio.chunkid, logbufferio.chunkid)

    @classmethod
    def new(cls, io, INDEX_COUNT=50, BUFFER_SIZE=10000):
        chunkfile = ChunkFile(io)
        chunkfile.append_chunk( LOG_INDEX_NAME, INDEX_COUNT * LogIndexEntrySerializer.SERIALIZED_LENGTH)
        chunkfile.append_chunk( LOG_BUFFER_NAME, BUFFER_SIZE )
        #Setup log index and log buffer
        logindexio = ChunkIO.from_name(chunkfile, LOG_INDEX_NAME)
        logindex_reader = LogIndexReader(logindexio, INDEX_COUNT)
        logindex = SerializedLogIndex.new(logindex_reader)
        
        logbufferio = ChunkIO.from_name(chunkfile,LOG_BUFFER_NAME)
        
        buffer_reader = LogBufferReader(logbufferio, logbufferio.size)
        logbuffer = LogBuffer(buffer_reader)
        return cls(chunkfile, logindex, logbuffer, logindexio.chunkid, logbufferio.chunkid)

        
class TransactionalIO(object):
    """ Transactionally read and write a single Chunk.
        E.g. Allows to write outpoints or privatekeys transactionaly
    """
    def __init__(self, txchunkfile, chunkid, chunkheader):
        self.txchunkfile = txchunkfile
        self.chunkid = chunkid
        self.chunkheader = chunkheader
        self.size = self.chunkheader.length

    def write(self, address, data):
        return self.txchunkfile.write(self.chunkid, address, data)
    
    def read(self, address, length):
        return self.txchunkfile.read(self.chunkid, address, length)
    
    @classmethod
    def from_chunkname(cls, txchunkfile, name):
        chunkpos, chunkheader = txchunkfile.chunkfile.get_chunk(name) 
        return cls(txchunkfile, chunkpos, chunkheader)


