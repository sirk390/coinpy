from coinpy.lib.wallet.formats.btc.serialization import ChunkHeaderSerializer


class ChunkReader(object):
    """ Go through a file, read and deserialize ChunkHeader's """
    def __init__(self):
        pass
        
    @staticmethod
    def readheader(iohandle, pos):
        """ Read and returm a ChunkHeader from the position `pos` in the file 
            Returns None if the file is too short.
        """ 
        chunk_header_data = iohandle.read(pos, ChunkHeaderSerializer.SERIALIZED_LENGTH)
        if len(chunk_header_data) == ChunkHeaderSerializer.SERIALIZED_LENGTH:
            return ChunkHeaderSerializer.deserialize(chunk_header_data)

    @staticmethod
    def iterchunkheaders(iohandle):
        pos = 0
        chunk_header = ChunkReader.readheader(iohandle, pos)
        while chunk_header:
            total_length = ChunkHeaderSerializer.SERIALIZED_LENGTH + chunk_header.length
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
