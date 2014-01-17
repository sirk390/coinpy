from io import SEEK_CUR
import os
from coinpy.lib.wallet.formats.btc.serialization import ItemHeaderSerializer,\
    ChunkHeaderSerializer, AllocSerializer, LogHeaderSerializer,\
    LogIndexEntrySerializer, OutpointIndexSerializer
from coinpy.lib.wallet.formats.btc.file_model import ItemHeader, Alloc, Log
import heapq
from coinpy.lib.serialization.structures.s11n_outpoint import OutpointSerializer


class FixedSizeEntryReader(object):
    """ Read and writes an IO containing a {nbentries} fixed size serialized entries 
        This is used for LogIndex.
        
        Could this use array API?
    """
    def __init__(self, io, nbentries, serializer):
        self.io = io
        self.nbentries = nbentries
        self.serializer = serializer
        self.serialized_length = self.serializer.SERIALIZED_LENGTH
        
    def iterentries(self):
        for i in range(self.nbentries):
            yield self.read_entry(i)

    def write_entry(self, pos, entry):
        if not (0 <= pos < self.nbentries):
            raise Exception("write_entry: position %d is not in range" % pos)
        self.io.write(pos*self.serializer.SERIALIZED_LENGTH, self.serializer.serialize(entry))

    def read_entry(self, pos):
        if not (0 <= pos < self.nbentries):
            raise Exception("read_entry: position %d is not in range" % pos)
        data = self.io.read(pos*self.serialized_length,self.serialized_length)
        return self.serializer.deserialize(data)

def LogIndexReader(io, nbentries):
    return FixedSizeEntryReader(io, nbentries, LogIndexEntrySerializer)
        

class InsufficientSpaceException(Exception):
    pass

class AllocatedRange(object):
    #rename to SerilializedDict? / KeySerializer for AllocSerializer
    def __init__(self, io, iosize, allpos=None, serializer=AllocSerializer):
        self.io = io
        self.iosize = iosize
        self.allpos = allpos or {}
        self.serializer = serializer
        self.header_size = self.serializer.SERIALIZED_LENGTH

    @classmethod
    def load(cls, io, iosize, serializer=AllocSerializer):
        allpos = dict(cls.readallocs(io, iosize, serializer))
        return cls( io, iosize, allpos, serializer)

    @classmethod
    def new(cls, io, iosize, serializer=AllocSerializer):
        """ could be moved to a function """
        header = Alloc(empty=True, size=iosize - serializer.SERIALIZED_LENGTH)
        io.write(0, serializer.serialize(header))
        return cls(io, iosize, {0: header}, serializer)

    def find_empty_location(self, length):
        for pos, alloc in self.allpos.iteritems():
            if alloc.empty and alloc.size >= length + self.header_size:
                return pos
    @classmethod
    def readallocs(cls, io, iosize, serializer):
        pos = 0
        while pos + serializer.SERIALIZED_LENGTH <= iosize:
            header = cls.read(io, pos, serializer)
            yield (pos, header)
            pos += serializer.SERIALIZED_LENGTH + header.size

    def iteritems(self):
        for pos, header in self.allpos.iteritems(): 
            yield pos, header

    def iterposvalues(self):
        for pos, header in self.allpos.iteritems():
            if not header.empty:
                yield pos, self.readobject(pos)

    def itervalues(self):
        for pos, header in self.allpos.iteritems():
            if not header.empty:
                yield self.readobject(pos)
            
    def readobject(self, pos):
        header = self.allpos[pos]
        return self.io.read(pos + self.serializer.SERIALIZED_LENGTH, header.size)
        
    @classmethod
    def read(cls, io, pos, serializer):
        headerdata = io.read(pos, serializer.SERIALIZED_LENGTH)
        header = serializer.deserialize(headerdata)
        return header

    def add(self, id, data):
        pos = self.find_empty_location(len(data))
        if pos is None:
            raise InsufficientSpaceException("Not enough space for data")
        self.insert(pos, id, data)
        return pos
        
    def insert(self, pos, id, data):
        """ Replace an empty location at {pos} by {data} """
        assert self.allpos[pos].empty
        oldemptyheader = self.allpos[pos]
        newobjheader = Alloc(empty=False, id=id, size=len(data))
        newemptylocationheader = Alloc(True, oldemptyheader.size - len(data) - self.serializer.SERIALIZED_LENGTH)
        newdata = (self.serializer.serialize(newobjheader) + 
                   data +
                   self.serializer.serialize(newemptylocationheader))
        self.io.write(pos, newdata)
        self.allpos[pos] = newobjheader
        self.allpos[pos + self.serializer.SERIALIZED_LENGTH + len(data)] = newemptylocationheader

    def remove_merging_with_next(self, pos, nextpos):
        header = self.allpos[pos]
        nextheader = self.allpos[nextpos]
        assert not header.empty
        assert nextheader.empty
        newemptyheader = Alloc(empty=True, size=header.size + self.serializer.SERIALIZED_LENGTH + nextheader.size)
        self.io.write(pos, self.serializer.serialize(newemptyheader) + 
                      "\x00" * (header.size + self.serializer.SERIALIZED_LENGTH)) #Note: erasing previous data
        self.allpos[pos] = newemptyheader
        del self.allpos[nextpos]

    def remove_merging_with_prev(self, pos, nextpos):
        header = self.allpos[pos]
        nextheader = self.allpos[nextpos]
        newemptyheader = Alloc(empty=True, size=header.size + self.serializer.SERIALIZED_LENGTH + nextheader.size)
        self.io.write(pos, self.serializer.serialize(newemptyheader))
        self.io.write(nextpos, "\x00" * (nextheader.size + self.serializer.SERIALIZED_LENGTH)) #Note: erasing previous data
        self.allpos[pos] = newemptyheader
        del self.allpos[nextpos]

    def remove_nomerge(self, pos):
        header = self.allpos[pos]
        header.empty = True

        self.io.write(pos, self.serializer.serialize(header) + 
                           "\x00" * header.size)
        self.allpos[pos] = header
    
    def getallocs(self):
        return [v for k,v in sorted(self.allpos.items(), key=lambda (k,v):k)]


    def remove(self, pos):
        nextpos = self._nextpos(pos)
        if nextpos is not None and self.is_empty(nextpos):
            return self.remove_merging_with_next(pos, nextpos)
        prevpos = self._prevpos(pos)
        if prevpos is not None and self.is_empty(prevpos):
            return self.remove_merging_with_prev(prevpos, pos)
        return self.remove_nomerge(pos)
        
    def is_empty(self, pos):
        return self.allpos[pos].empty

    # TODO: improve using some sorted structure.
    def _nextpos(self, pos):
        sortedpos = sorted(self.allpos) 
        for i, p in enumerate(sortedpos):
            if p == pos and i+1 < len(sortedpos):
                return sortedpos[i+1]
    def _prevpos(self, pos):
        sortedpos = sorted(self.allpos)
        for i, p in enumerate(sortedpos):
            if p == pos:
                return sortedpos[i-1] if i else None
    
class SerializedObjectDict(object):
    """ Read and writes an IO containing a variable number of unordered entries.
        This is used for OutpointIndex, PrivateKeys, ...
    """
    def __init__(self, allocated, objects, serializer):
        self.allocated = allocated
        self.objects = objects
        self.serializer = serializer

    @classmethod
    def new(cls, io, iosize, serializer):
        allocated = AllocatedRange.new(io, iosize)
        return cls(allocated, {}, serializer)
           
    @classmethod
    def load(cls, io, iosize, serializer):
        allocated = AllocatedRange.load(io, iosize)
        objects = {}
        for pos, header in allocated.iteritems():
            if not header.empty:
                objects[header.id] = (pos, serializer.deserialize(allocated.readobject(pos)))
        return cls(allocated, objects, serializer)
    
    def iteritems(self):
        for id, (pos, obj) in self.objects.iteritems():
            yield id, obj
        
    def set(self, id, obj):
        data = self.serializer.serialize(obj)
        if id in self.objects:
            self.allocated.remove(id)
        pos = self.allocated.add(id, data)
        self.objects[id] = (pos, obj)
    
    def remove(self, id):
        pos, obj = self.objects[id]
        del self.objects[id]
        self.allocated.remove(pos)



class LogBufferReader(object):
    """ Read and writes an IO
        
        This is used for LogBuffer.
    """
    def __init__(self, io, iosize, serializer=LogHeaderSerializer):
        self.io = io
        self.iosize = iosize
        self.serializer = serializer

    def get_size(self, log):
        return self.serializer.SERIALIZED_LENGTH + (2*log.logheader.length)
    
    def write_entry(self, pos, log):
        logheader = self.serializer.serialize(log.logheader)
        totallength = self.serializer.SERIALIZED_LENGTH + (2*log.logheader.length)
        if not (0 <= pos and  pos + totallength < self.iosize):
            raise Exception("write_entry: out of range (pos=%d, datalength=%d, iosize:%d)" % (pos,  totallength, self.iosize))
        self.io.write(pos, logheader + log.data + log.original_data)
        return totallength

    def read_entry(self, pos):
        data = self.io.read(pos, self.serializer.SERIALIZED_LENGTH)
        logheader = self.serializer.deserialize(data)
        totallength = self.serializer.SERIALIZED_LENGTH + (2*logheader.length)
        if not (0 <= pos + totallength < self.iosize):
            raise Exception("read_entry: out of range (pos=%d, datalength=%d, iosize:%d)" % (pos,  totallength, self.iosize))
        data = self.io.read(pos+self.serializer.SERIALIZED_LENGTH, 2*logheader.length)
        return (Log(logheader, data[:logheader.length], data[logheader.length:]), totallength)

    
class ChunkReader(object):
    """ Go through a file, read and deserialize ChunkHeader's """
    def __init__(self):
        pass
        
    @staticmethod
    def readheader(iohandle, pos):
        """ Read and returm a ChunkHeader from the position `pos` in the file 
            Returns None if the file is too short.
        """ 
        chunk_header_data = iohandle.read(pos, ChunkHeaderSerializer.CHUNKHEADER_SIZE)
        if len(chunk_header_data) == ChunkHeaderSerializer.CHUNKHEADER_SIZE:
            return ChunkHeaderSerializer.deserialize(chunk_header_data)

    @staticmethod
    def iterchunkheaders(iohandle):
        pos = 0
        chunk_header = ChunkReader.readheader(iohandle, pos)
        while chunk_header:
            total_length = ChunkHeaderSerializer.CHUNKHEADER_SIZE + chunk_header.length
            yield pos, chunk_header
            pos += total_length
            chunk_header = ChunkReader.readheader(iohandle, pos)

'''

class ChunkItemLoader(object):
    """ Go through a chunk, read items's """
    def __init__(self):
        pass
        
    @classmethod
    def readheader(cls, iohandle, pos):
        """ Read and returm a ChunkHeader from the position `pos` in the file 
            Returns None if the file is too short.
        """ 
        chunk_header_data = iohandle.read(pos, ItemHeaderSerializer.SERIALIZED_LENGTH)
        return ItemHeaderSerializer.deserialize(chunk_header_data)

    @classmethod
    def iterchunkitems(cls, iohandle, pos, max_pos):
        while pos < max_pos:
            itemheader = cls.readheader(iohandle, pos)
            yield pos, itemheader
            pos += cls.SERIALIZED_LENGTH + itemheader.data_length
 

'''
