import unittest
import StringIO
import mock
from coinpy.lib.wallet.formats.btc.chunk_file import ChunkFile
from io import SEEK_END


class TestChunkFile(unittest.TestCase):
    def test_ChunkFile_NewChunkFile_ContainsNoChunk(self):
        io = StringIO.StringIO()
        chunk_file = ChunkFile(io)
        
        
    def test_ChunkFile_AppendAChunk_IOSeeksAndIOWriteAreCalledInSequence(self):
        iocalls = mock.Mock()
        io = mock.Mock()
        io.seek = lambda *args: iocalls("seek", *args)
        io.write = lambda *args, **kwargs: iocalls("write", *args, **kwargs)
        stubSerializer = mock.Mock(serialize=mock.Mock(return_value=""))
        chunk_file = ChunkFile(io, serializer=stubSerializer)
        
        chunk_file.append_chunk(name="", length=0, version=0)

        iocalls.assert_has_calls( [mock.call("seek", 0, SEEK_END),
                                   mock.call("write", data="") ])


        
if __name__ == "__main__":
    unittest.main()
