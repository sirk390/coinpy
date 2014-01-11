from itertools import ifilter, groupby
from collections import namedtuple
import collections
from pydoc import deque
from coinpy.tools.event import Event
from coinpy.tools.functools import rindex, lindex
from coinpy.lib.wallet.formats.btc.serialization import LogIndexEntrySerializer
from coinpy.lib.wallet.formats.btc.entry_reader import FixedSizeEntryReader

CHUNK_SIZE=16

from coinpy.lib.wallet.formats.btc.file_model import LogIndexEntry, Log,\
    LogHeader

def LogIndexReader(io, nbentries):
    return FixedSizeEntryReader(io, nbentries, LogIndexEntrySerializer)
        
class CorruptLogIndexException(Exception):
    pass

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
            self.ON_COMMITING.fire(logidx)
        logidx.needs_commit = False    
        self.ON_COMMITED.fire(logidx)

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

    def on_commited(self, logindex):
        self.logindex_reader.write_entry(self.start_pos, logindex)
        self.start_pos += 1
        if not self.tocommit:
            self.start_pos = 0

    @staticmethod
    def new(logindex_reader):
        for i in range(logindex_reader.nbentries):
            logindex_reader.write_entry(i, LogIndexEntry(LogIndexEntry.WRITE, needs_commit=False))
        return SerializedLogIndex(logindex_reader)
    
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

class TransactionLog(object):
    """
        writelogs (dict (int,int) => Log): Dictionnary mapping from (start_offset, end_offset) in LogBuffer to Log instance.
    """
    def __init__(self, io, logindex, logbuffer):
        self.io = io
        self.logindex = logindex
        self.logbuffer = logbuffer

    def recover(self):
        self.logindex.recover()

    def start_transaction(self):
        self.logindex.log(LogIndexEntry(LogIndexEntry.BEGIN_TX))

    def write(self, address, data):
        size = len(data)
        log = Log(LogHeader(address, len(data)), data, self.io.read(address, size))
        bufferpos = self.logbuffer.find_empty_location_for_log(log)
        self.logbuffer.write_entry(bufferpos, log)
        self.logindex.log(LogIndexEntry(LogIndexEntry.WRITE, bufferpos))

    def commit_transaction(self):
        self.logindex.log(LogIndexEntry(LogIndexEntry.END_TX))

class TransactionalFile(object):
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
        self.log.start_transaction()
    
    def write(self, address, data):
        self.log.write(address, data)
    
    
    
        
