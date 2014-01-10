import unittest
import mock
from coinpy.lib.wallet.formats.btc.file_model import LogIndexEntry
from coinpy.lib.wallet.formats.btc.transactional import CorruptLogIndexException, logindex_parse_groups, TransactionLog,\
    LogIndexReader, SerializedLogIndex
from coinpy.lib.wallet.formats.btc.file_handle import IoHandle
from coinpy.lib.wallet.formats.btc.serialization import LogIndexEntrySerializer
from pydoc import deque



def makeLogIndexReader(entries=[]):
    return  mock.Mock(iterentries = mock.Mock(return_value=entries))


class TestLogIndex(unittest.TestCase):
    def test_ParseLogIndexGroups_ParseEmptyArray_ReturnsEmptyArray(self):
        logidx = []
        
        result = logindex_parse_groups(logidx)
        
        self.assertEquals(result, ([],[]))
        
    def test_ParseLogIndexGroups_ParseWrite_ReturnsOneArrayWithOneIndex(self):
        logidx = [LogIndexEntry.WRITE]
        
        result = logindex_parse_groups(logidx)
        
        self.assertEquals(result, ([[0]], []))

    def test_ParseLogIndexGroups_ParseTwoWrite_ReturnsTwoArraysWithEachOneIndex(self):
        logidx = [LogIndexEntry.WRITE, LogIndexEntry.WRITE]

        result = logindex_parse_groups(logidx)
        
        self.assertEquals(result, ([[0], [1]], []))

    def test_ParseLogIndexGroups_ParseBeginTxTwice_RaisesCorruptLogIndexException(self):
        logidx = [LogIndexEntry.BEGIN_TX, LogIndexEntry.BEGIN_TX]
        
        with self.assertRaises(CorruptLogIndexException):
            logindex_parse_groups(logidx)

    def test_ParseLogIndexGroups_ParseEndTxTwice_RaisesCorruptLogIndexException(self):
        logidx = [LogIndexEntry.END_TX, LogIndexEntry.END_TX]
        
        with self.assertRaises(CorruptLogIndexException):
            logindex_parse_groups(logidx)


    def test_ParseLogIndexGroups_ParseTransaction_ReturnsIndexesBothInOneArray(self):
        logidx = [LogIndexEntry.BEGIN_TX, LogIndexEntry.END_TX]

        result = logindex_parse_groups(logidx)

        self.assertEquals(result, ([[0,1]], []))

    def test_ParseLogIndexGroups_ParseTwoTransactions_ReturnsIndexesBothInTwoArrays(self):
        logidx = [LogIndexEntry.BEGIN_TX, LogIndexEntry.END_TX, LogIndexEntry.BEGIN_TX, LogIndexEntry.END_TX]

        result = logindex_parse_groups(logidx)

        self.assertEquals(result, ([[0,1], [2,3]], []))

    def test_ParseLogIndexGroups_ParseWriteInTransaction_ReturnsIndexesInOneArray(self):
        logidx = [LogIndexEntry.BEGIN_TX, LogIndexEntry.WRITE, LogIndexEntry.END_TX]

        result = logindex_parse_groups(logidx)

        self.assertEquals(result, ([[0,1,2]], []))
        
    def test_ParseLogIndexGroups_ParseWriteOutsideTransaction_ReturnsWriteIndexSeparately(self):
        logidx = [LogIndexEntry.BEGIN_TX, LogIndexEntry.END_TX, LogIndexEntry.WRITE]

        result = logindex_parse_groups(logidx)

        self.assertEquals(result, ([[0,1], [2]], []))

    def test_ParseLogIndexGroups_ParseUnclosedTransactions_ReturnsAsIncomplete(self):
        logidx = [LogIndexEntry.BEGIN_TX]

        result = logindex_parse_groups(logidx)

        self.assertEquals(result, ([], [0]))

    def test_ParseLogIndexGroups_ParseUnclosedTransactionWriteWrite_ReturnsInLastArray(self):
        logidx = [LogIndexEntry.BEGIN_TX, LogIndexEntry.WRITE]

        result = logindex_parse_groups(logidx)

        self.assertEquals(result, ([], [0, 1]))




class TestSerializedLogIndex(unittest.TestCase):
    def test_SerializedLogIndex_recover_ErasesLastUnfinishedTransaction(self):
        COUNT = 10
        io = IoHandle.using_stringio(COUNT)
        reader = LogIndexReader(io, COUNT)
        logindex = SerializedLogIndex.new(reader)
        logindex.log(LogIndexEntry(LogIndexEntry.BEGIN_TX))
        logindex.log(LogIndexEntry(LogIndexEntry.WRITE, 1))
        logindex.log(LogIndexEntry(LogIndexEntry.WRITE, 2))
        logindex.log(LogIndexEntry(LogIndexEntry.END_TX))
        logindex.log(LogIndexEntry(LogIndexEntry.BEGIN_TX))
        logindex.log(LogIndexEntry(LogIndexEntry.WRITE, 3))
        logindex.log(LogIndexEntry(LogIndexEntry.WRITE, 4))
        logindex2 = SerializedLogIndex.load(reader)
        
        logindex2.recover()
        
        self.assertEquals(logindex2.tocommit, 
                          deque([ LogIndexEntry(LogIndexEntry.BEGIN_TX),
                                  LogIndexEntry(LogIndexEntry.WRITE, 1),
                                  LogIndexEntry(LogIndexEntry.WRITE, 2),
                                  LogIndexEntry(LogIndexEntry.END_TX)] ))
        
class TestTxChunkFile(unittest.TestCase):
    """def test_WalletFile_(self):
        
        file = TxChunkFile(io, )
        file.addLogIndexEntry(LogIndexEntry(LogIndexEntry.BEGIN_TX))
        file.addlogentry()
        
    def test_WalletFile_Loader(self):
        chunkfile = ChunkFile(io=mock.Mock(), chunk_locations=[(10,  ChunkHeader(type=LOG_INDEX, version=1, length=100)),
                                                               (110, ChunkHeader(type=LOG_BUFFER, version=1, length=100)),
                                                               (210, ChunkHeader(type=KEYS, version=1, length=500))])
        chunkfile.write(chunk=1, pos=10, "jiij") #t1
        chunkfile.fixchecksum(chunk=1) #t2"""
        
    '''
    def test_TxChunkFile_WhenCalllingStartTransaction_WritesANewLogIndexEntry(self):
        log_index = makeFakeLogIndex()
        logbuffer = mock.Mock(iterentries = mock.Mock(return_value=[]))        
        txchunkfile = TxChunkFile(io=mock.Mock(), LogIndexEntry=LogIndexEntry, logbuffer=logbuffer)
        
        txchunkfile.start_transaction()
        
        log_index.write_entry.assert_called_once_with(0, LogIndexEntry(BEGIN_TX))

    def test_TxChunkFile_WhenWritingData_LocateEmptyLogBuffer(self):
        TEST_DATA="test1"
        TEST_ADDRESS=0
        log_index = mock.Mock(iterentries = mock.Mock(return_value=[]),
                              allocate_buffer = mock.Mock(return_value="location1"))
        logbuffer = mock.Mock(iterentries = mock.Mock(return_value=[]))        
        txchunkfile = TxChunkFile(io=mock.Mock(), LogIndexEntry=LogIndexEntry, logbuffer=logbuffer)
        
        txchunkfile.write(address=TEST_ADDRESS, data=TEST_DATA)
        
        log_index.allocate_buffer.assert_called_once_with(len(TEST_DATA))
        logbuffer.write.assert_called_once_with("location1", TEST_ADDRESS, TEST_DATA)
        


    '''
        
if __name__ == "__main__":
    unittest.main()
