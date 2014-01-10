
class FileHeader():
    def __init__(self, signature="\x89WLT\r\n\x1a\n", version=1):
        self.signature = signature
        self.version = version
        
    def __eq__(self, other):
        return (self.signature == other.signature and
                self.version == other.version)
    
LOG_INDEX, LOG_BUFFER, MASTER_KEYS, KEYS, OUTPOINTS, METADATA, ACCOUNTS, UNSUBMITTED_TX = CHUNK_TYPES = range(8)

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

class Alloc(object):
    def __init__(self, empty, size):
        self.size = size
        self.empty = empty
        
    def __eq__(self, other):
        return (self.empty == other.empty and
                self.size == other.size)
        
    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, " ".join("%s:%s" % (k,v) for k,v in  self.__dict__.items()))
   
class ItemHeader(object):
    def __init__(self, empty, id, size):
        self.empty = empty
        self.id = id
        self.size = size
        
    def __eq__(self, other):
        return (self.empty == other.empty and
                self.id == other.id and
                self.size == other.size)
        
    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, " ".join("%s:%s" % (k,v) for k,v in  self.__dict__.items()))


class ChunkInfo(object):
    def __init__(self, type, version=1, length=0, objects=0):
        self.type = type
        self.version = version
        self.length = length
        self.objects = objects

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

    def is_tx_command(self):
        return (self.command == LogIndexEntry.BEGIN_TX or 
                self.command == LogIndexEntry.END_TX)
        
    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, " ".join("%s:%s" % (k,v) for k,v in  self.__dict__.items()))
                
class LogIndexChunk(object):
    def __init__(self, entries):
        pass
    
class LogBufferChunk(object):
    def __init__(self, size):
        pass
    
class KeysChunk(object):
    def __init__(self, size):
        pass

class OutpointsChunk(object):
    def __init__(self, size):
        pass

class WalletFile(object):
    def __init__(self, file_header, log_index_chunk, log_buffer_chunk, keys_chunk, outpoints_chunk, metadata_chunk):
        self.file_header = file_header
        self.log_index_chunk = log_index_chunk
        self.log_buffer_chunk = log_buffer_chunk
        self.keys_chunk = keys_chunk
        self.outpoints_chunk = outpoints_chunk
        self.metadata_chunk = metadata_chunk

class MetadataChunk():
    def __init__(self, metadata):
        self.metadata = metadata

class Metadata():
    def __init__(self, wallet_id, comment):
        self.wallet_id = wallet_id
        self.comment = comment

class Log(object):
    """ Entry in the write ahead log buffer` """
    def __init__(self, address, data, original_data):
        self.address = address
        self.data = data
        self.original_data = original_data
        
    def __eq__(self, other):
        return (self.address == other.address and
                self.data == other.data and
                self.original_data == other.original_data)

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__, " ".join("%s:%s" % (k,v) for k,v in  self.__dict__.items()))
       
