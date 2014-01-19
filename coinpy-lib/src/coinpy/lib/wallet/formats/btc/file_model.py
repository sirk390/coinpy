
class FileHeader():
    def __init__(self, signature="\x89WLT\r\n\x1a\n", version=1):
        self.signature = signature
        self.version = version
     
    def __repr__(self):
        return "<FileHeader version:%d>" % (self.version)
    
    def __eq__(self, other):
        return (self.signature == other.signature and
                self.version == other.version)
    
LOG_INDEX, LOG_BUFFER, MASTER_KEYS, KEYS, OUTPOINTS, METADATA, ACCOUNTS, UNSUBMITTED_TX = CHUNK_TYPES = range(8)

LOG_INDEX_NAME= "ILOG"
LOG_BUFFER_NAME= "bLOG"
OUTPOINTS_NAME = "pOUT"
CHUNK_NAMES = {LOG_INDEX:LOG_INDEX_NAME, 
               LOG_BUFFER:LOG_BUFFER_NAME, 
               MASTER_KEYS:"mKEY", 
               KEYS:"sKEY", 
               OUTPOINTS: OUTPOINTS_NAME, 
               METADATA:"iNFO",
               ACCOUNTS:"aCNT", 
               UNSUBMITTED_TX:"uTXS"}

class ChunkHeader(object):
    def __init__(self, name, version, length, crc):
        self.name = name
        self.version = version
        self.length = length
        self.crc = crc
        
    def __eq__(self, other):
        return (self.name == other.name and
                self.version == other.version and
                self.length == other.length and
                self.crc == other.crc)

class ItemHeader(object):
    def __init__(self, empty, size):
        self.size = size
        self.empty = empty
        
    def __eq__(self, other):
        return (self.empty == other.empty and
                self.size == other.size)
        
    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, " ".join("%s:%s" % (k,v) for k,v in  self.__dict__.items()))

class LogIndexEntry(object):
    BEGIN_TX, END_TX, WRITE, CHANGE_FILESIZE = COMMANDS = range(4)
    """ Entry in the write ahead log index """
    def __init__(self, command, argument=0, needs_commit=True):
        self.command = command
        self.argument = argument
        self.needs_commit = needs_commit
        
    def __eq__(self, other):
        return (self.command == other.command and
                self.argument == other.argument and
                self.needs_commit == other.needs_commit)
    
    def is_write(self):
        return (self.command == LogIndexEntry.WRITE)
    
    def is_tx_command(self):
        return (self.command == LogIndexEntry.BEGIN_TX or 
                self.command == LogIndexEntry.END_TX)
        
    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, " ".join("%s:%s" % (k,v) for k,v in  self.__dict__.items()))



class Metadata():
    def __init__(self, wallet_id, comment):
        self.wallet_id = wallet_id
        self.comment = comment

class LogHeader(object):
    """ Header for entries in the write ahead log buffer` """
    def __init__(self, chunk, address, length):
        self.chunk = chunk
        self.address = address
        self.length = length

    def __eq__(self, other):
        return (self.chunk == other.chunk and
                self.address == other.address and
                self.length == other.length)

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, " ".join("%s:%s" % (k,v) for k,v in  self.__dict__.items()))

class Log(object):
    """ Entry in the write ahead log buffer` """
    def __init__(self, logheader, data, original_data):
        self.logheader = logheader
        self.data = data
        self.original_data = original_data
        assert(self.logheader.length == len(data)), "data must have the correct length"
        assert(self.logheader.length == len(original_data)), "original_data must have the correct length"

    def __eq__(self, other):
        return (self.logheader == other.logheader and
                self.data == other.data and
                self.original_data == other.original_data)

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, " ".join("%s:%s" % (k,v) for k,v in  self.__dict__.items()))

