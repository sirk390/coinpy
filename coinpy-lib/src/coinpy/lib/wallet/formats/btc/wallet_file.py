from coinpy.lib.wallet.formats.btc.file_model import FileHeader, WalletFile,\
    LogIndexChunk, KeysChunk, LogBufferChunk, OutpointsChunk, Metadata,\
    MetadataChunk, LOG_INDEX_NAME, ChunkHeader, CHUNK_NAMES, LOG_BUFFER, OUTPOINTS,\
    LOG_BUFFER_NAME, OUTPOINTS_NAME
from coinpy.lib.wallet.formats.btc.wallet_model import BtcWallet, Delete, Set,\
    ItemSet
from coinpy.lib.wallet.formats.btc.file_handle import IoHandle
from coinpy.lib.wallet.formats.btc.entry_reader import  LogBufferReader, LogIndexReader, SerializedObjectDict
from coinpy.lib.wallet.formats.btc.transactional import LogBuffer,\
    SerializedLogIndex, LogIndex, TransactionLog,\
    TransactionalIO
from coinpy.lib.wallet.formats.btc.serialization import LogIndexEntrySerializer,\
    OutpointIndexSerializer, ChunkHeaderSerializer, FileHeaderSerializer
from coinpy.lib.wallet.formats.btc.chunk_file import ChunkFile
import zlib


def new_empty_walletfile():
    return WalletFile( FileHeader(version=1),
                       chunks = [LogIndexChunk( nb_entries=100 ),
                                 LogBufferChunk( size=100*1024 ),
                                 KeysChunk( size=100*1024 ),
                                 OutpointsChunk( size=100*1024 ),
                                 MetadataChunk( Metadata("\0" ** 32, comment="New Wallet"))]
                        )

class SerializedItemSet( ItemSet ):
    def __init__(self, serialized_dict, items_by_key=None):
        super(SerializedItemSet, self).__init__(items_by_key)
        self.ON_CHANGING.subscribe(self.on_changing)
        self.serialized_dict = serialized_dict
    
    def on_changing(self, event):
        key = event.key
        #print "on_changing"
        if type(event.change) == Delete: 
            self.serialized_dict.remove(key)
        if type(event.change) == Set: 
            self.serialized_dict.set(key, event.change.value)
            
    @classmethod
    def load(cls, serialized_dict):
        #VarSizeEntryReader
        items_by_key = {}
        for id, obj in serialized_dict.iteritems():
            items_by_key[id] = obj
        return SerializedItemSet(serialized_dict, items_by_key)
    

class WalletFile(object):
    def __init__(self, txlog, outpoint_dict):
        self.txlog = txlog
        self.outpoints = outpoint_dict
        
    def start_tx(self):
        self.txlog.start_transaction()
    
    def end_tx(self):
        self.txlog.end_transaction()

    @classmethod
    def load(cls, io, iosize):
        chunkfile = ChunkFile.open(io, iosize)
        _, logindexheader, logindexio = chunkfile.open_chunk(LOG_INDEX_NAME)
        _, logbufferheader, logbufferio = chunkfile.open_chunk(LOG_BUFFER_NAME)
       
        logindex_reader = LogIndexReader(logindexio, logindexheader.length/LogIndexEntrySerializer.SERIALIZED_LENGTH)
        logindex = SerializedLogIndex.load(logindex_reader)

        logbuffer_reader = LogBufferReader(logbufferio, logbufferheader.length)
        logbuffer = LogBuffer.load(logindex, logbuffer_reader)
        
        txlog = TransactionLog(chunkfile, logindex, logbuffer)
        
        outpointchunk, outpointchunkheader = chunkfile.get_chunk(OUTPOINTS_NAME) 
        outpoint_io = TransactionalIO(txlog, outpointchunk)
        outpoint_dict = SerializedObjectDict.load(outpoint_io, outpointchunkheader.length, serializer=OutpointIndexSerializer)
        return cls(txlog, outpoint_dict)

    @classmethod
    def new(cls, io):
        IO_SIZE = 1000
        BUFFER_SIZE = 10000
        INDEX_COUNT = 50
        OUTPOINTS_SIZE = 1000
        
        fileheader = FileHeader()
        io.write(FileHeaderSerializer.serialize(fileheader))
        #write chunks
        chunkfile = ChunkFile(io)
        chunkfile.append_chunk( LOG_INDEX_NAME, INDEX_COUNT * LogIndexEntrySerializer.SERIALIZED_LENGTH)
        chunkfile.append_chunk( LOG_BUFFER_NAME, BUFFER_SIZE )
        chunkfile.append_chunk( OUTPOINTS_NAME, OUTPOINTS_SIZE )
        #Load log index and log buffer
        _, _logindexheader, logindexio = chunkfile.open_chunk(LOG_INDEX_NAME)
        logindex_reader = LogIndexReader(logindexio, INDEX_COUNT)

        logindex = SerializedLogIndex.new(logindex_reader)
        _, logbufferheader, logbufferio = chunkfile.open_chunk(LOG_BUFFER_NAME)
        buffer_reader = LogBufferReader(logbufferio, logbufferheader.length)
        logbuffer = LogBuffer(buffer_reader)
        # format other chunks ( not transactionally)
        _, outpointsheader, outpointsio = chunkfile.open_chunk(OUTPOINTS_NAME)
        outpoint_dict = SerializedObjectDict.new(outpointsio, outpointsheader.length, serializer=OutpointIndexSerializer)
        SerializedItemSet.load(outpoint_dict)
        # 
        txlog = TransactionLog(chunkfile, logindex, logbuffer)

        outpointchunk, outpointchunkheader = chunkfile.get_chunk(OUTPOINTS_NAME) 
        outpoint_io = TransactionalIO(txlog, outpointchunk)
        outpoint_dict = SerializedObjectDict.load(outpoint_io, OUTPOINTS_SIZE, OutpointIndexSerializer)
        return cls(txlog, outpoint_dict)


class SerilializedWallet(BtcWallet):
    def __init__(self, wallet_file ):
        self.wallet_file = wallet_file
        
        super(SerilializedWallet, self).__init__( outpoints = outpoints)
        self.ON_STARTING_TX.subscribe(self.on_starting_tx)
        self.ON_ENDING_TX.subscribe(self.on_ending_tx)
    
    def on_starting_tx(self, event):
        self.txlog.start_transaction()
    
    def on_ending_tx(self, event):
        self.txlog.end_transaction()

    @classmethod
    def load(cls, io):
        chunkfile = ChunkFile.open(io)
        _, logindexheader, logindexio = chunkfile.open_chunk(LOG_INDEX_NAME)
        _, logbufferheader, logbufferio = chunkfile.open_chunk(LOG_BUFFER_NAME)
       
        logindex_reader = LogIndexReader(logindexio, logindexheader.length/LogIndexEntrySerializer.SERIALIZED_LENGTH)
        logindex = SerializedLogIndex.load(logindex_reader)

        logbuffer_reader = LogBufferReader(logbufferio, logbufferheader.length)
        logbuffer = LogBuffer.load(logindex, logbuffer_reader)
        
        txlog = TransactionLog(chunkfile, logindex, logbuffer)
        
        outpointchunk, outpointchunkheader = chunkfile.get_chunk(OUTPOINTS_NAME) 
        outpoint_io = TransactionalIO(txlog, outpointchunk)
        outpoint_reader = OutpointIndexReader(outpoint_io, outpointchunkheader.length)
        outpoints = SerializedItemSet.load(outpoint_reader)
        return cls(txlog, outpoints)

    @classmethod
    def new(cls, io):
        IO_SIZE = 1000
        BUFFER_SIZE = 10000
        INDEX_COUNT = 50
        OUTPOINTS_SIZE = 1000
        
        fileheader = FileHeader()
        io.write(FileHeaderSerializer.serialize(fileheader))
        #write chunks
        chunkfile = ChunkFile(io)
        chunkfile.append_chunk( LOG_INDEX_NAME, INDEX_COUNT * LogIndexEntrySerializer.SERIALIZED_LENGTH)
        chunkfile.append_chunk( LOG_BUFFER_NAME, BUFFER_SIZE )
        chunkfile.append_chunk( OUTPOINTS_NAME, OUTPOINTS_SIZE )
        #Load log index and log buffer
        _, _logindexheader, logindexio = chunkfile.open_chunk(LOG_INDEX_NAME)
        logindex_reader = LogIndexReader(logindexio, INDEX_COUNT)

        logindex = SerializedLogIndex.new(logindex_reader)
        _, logbufferheader, logbufferio = chunkfile.open_chunk(LOG_BUFFER_NAME)
        buffer_reader = LogBufferReader(logbufferio, logbufferheader.length)
        logbuffer = LogBuffer(buffer_reader)
        # format other chunks ( not transactionally)
        _, outpointsheader, outpointsio = chunkfile.open_chunk(OUTPOINTS_NAME)
        outpoint_dict = SerializedObjectDict.new(outpointsio, outpointsheader.length, serializer=OutpointIndexSerializer)
        SerializedItemSet.load(outpoint_dict)
        # 
        txlog = TransactionLog(chunkfile, logindex, logbuffer)

        outpointchunk, outpointchunkheader = chunkfile.get_chunk(OUTPOINTS_NAME) 
        outpoint_io = TransactionalIO(txlog, outpointchunk)
        outpoint_reader = SerializedObjectDict.load(outpoint_io, OUTPOINTS_SIZE, OutpointIndexSerializer)
        outpoints = SerializedItemSet.load(outpoint_reader)
        return cls(txlog, outpoints)



"""
class WalletBuilder(object):
    def new_wallet(self, io):
        wallet_file = new_empty_walletfile()
             
        io.write(WalletFileSerializer.serialize(wallet_file))


        wallet = BtcWallet ( )

        wallet.private_keys.ON_CHANGING.subscribe(self.on_changing_privatekeys)
"""