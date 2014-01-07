from io import SEEK_CUR
import os
from coinpy.lib.wallet.formats.btc.serialization import ItemHeaderSerializer,\
    ChunkHeaderSerializer, AllocSerializer
from coinpy.lib.wallet.formats.btc.file_model import ItemHeader, Alloc
import heapq


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
    


class AllocatedRange(object):
    def __init__(self, io, iosize, allocs=None, serializer=AllocSerializer):
        self.io = io
        self.iosize = iosize
        self.serializer = serializer
        self.allpos = allocs if allocs else {0:Alloc(empty=True, size=iosize)}
        self.header_size = self.serializer.SERIALIZED_LENGTH

    def find_empty_location(self, length):
        for pos, alloc in self.allpos.iteritems():
            if alloc.empty and alloc.size >= length + self.header_size:
                return pos

    def readall(self):
        pos = 0
        while pos + self.serializer.SERIALIZED_LENGTH <= self.iosize:
            header, data = self.read(pos)
            if data is not None:
                yield (pos, data)
            pos += self.serializer.SERIALIZED_LENGTH + header.size

    def read(self, pos):
        header = self.io.read(pos, self.serializer.SERIALIZED_LENGTH)
        if not header.empty:
            return header, self.io.read(pos + self.serializer.SERIALIZED_LENGTH, header.size)

    def add(self, data):
        pos = self.find_empty_location(len(data))
        if pos is None:
            raise Exception("Not enough space for data")
        self.insert(pos, data)
        return pos
        
    def insert(self, pos, data):
        """ Replace an empty location at {pos} by {data} """
        assert self.allpos[pos].empty
        oldemptyheader = self.allpos[pos]
        newobjheader = Alloc(empty=False, size=len(data))
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
                           "\x00" * (self.serializer.SERIALIZED_LENGTH + header.size))
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
    
class VarSizeEntryReader(object):
    """ Read and writes an IO containing a variable number of unordered entries.
        This is used for LogBuffer.
        
    """
    def __init__(self, io, iosize, serializer, new=False):
        self.io = io
        self.iosize = iosize
        self.serializer = serializer
        if new:
            self._new()
        else:
            self._open()
        self.objects
            
    
    def _new(self):
        header = ItemHeader(empty=True, id=0, size=self.iosize - self.alloc_serializer.SERIALIZED_LENGTH)
        self.io.write(0, self.alloc_serializer.serialize(header))
        self._add_empty_location(0, header)

    def _open(self):
        pos = 0
        while pos + self.alloc_serializer.SERIALIZED_LENGTH <= self.iosize:
            header, obj = self._readat(pos)
            if not header.empty:
                self._add_object(pos, header, obj)
            else:
                self._add_empty_location(pos, header)
            pos += self.alloc_serializer.SERIALIZED_LENGTH + header.size

    def iteritems(self):
        for id, (pos, header, obj) in self.objects.iteritems():
            yield id, obj
        
    def add(self, id, obj):
        pass
        
    def remove(self, id):
        pass
        
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
