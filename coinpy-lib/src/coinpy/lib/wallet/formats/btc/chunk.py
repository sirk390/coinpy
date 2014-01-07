from zipfile import crc32
from coinpy.lib.wallet.formats.btc.serialization import ChunkHeaderSerializer

class ChunkHandle( object ):
    """ Allows reading and writing to a specific chunk of the file (non transactionaly) """
    def __init__(self, iohandle, chunkheader, chunkheader_serializer=ChunkHeaderSerializer):
        self.iohandle = iohandle
        self.chunkheader = chunkheader
        self.chunkheader_serializer = chunkheader_serializer
    
    def write(self, pos, data):
        """Write relatively to the start of chunk, and update header crc"""
        self.iohandle.write(self.chunkheader_serializer.SERIALIZED_LENGTH + pos)
        data = self.iohandle.read(0, self.chunkheader.length)
        self.chunkheader.crc = crc32(data)
        serialized_header = self.chunkheader_serializer.serialize(self.chunkheader)
        self.iohandle.write(serialized_header)
        
    def read(self, pos, length):
        """Write relatively to the start of chunk"""
        return self.iohandle.read(self.chunkheader_serializer.SERIALIZED_LENGTH + pos)
        
 