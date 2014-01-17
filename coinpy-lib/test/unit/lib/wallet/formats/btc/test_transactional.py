import unittest
import mock
from coinpy.lib.wallet.formats.btc.file_model import LogIndexEntry
from coinpy.lib.wallet.formats.btc.transactional import CorruptLogIndexException, TransactionLog,\
     SerializedLogIndex, LogBuffer
from coinpy.lib.wallet.formats.btc.file_handle import IoHandle
from coinpy.lib.wallet.formats.btc.serialization import LogIndexEntrySerializer
from pydoc import deque
from coinpy.lib.wallet.formats.btc.entry_reader import LogBufferReader,\
    LogIndexReader
from coinpy.lib.wallet.formats.btc.chunk_file import MultiChunkIO



def makeLogIndexReader(entries=[]):
    return  mock.Mock(iterentries = mock.Mock(return_value=entries))



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


class TestLogBuffer(unittest.TestCase):
    def test_getunallocated_WithEmptyWriteLogs_ReturnsZeroToBufferSize(self):
        writelogs = {}
        logbuff = LogBuffer(mock.Mock(iosize=100), writelogs)
        
        self.assertEquals(logbuff.getunallocated(), [(0, 100)])
        
    def test_getunallocated_WithOneLogStartingAtBegining_ReturnsOnlyOneRangeAtTheEnd(self):
        logs = {(0,1) : "log1"}
        logbuff = LogBuffer(mock.Mock(iosize=2), logs)
        
        self.assertEquals(logbuff.getunallocated(), [(1, 2)])

    def test_getunallocated_WithOneLogEndingAtBufferSize_ReturnsOnlyOneRangeAtTheBeginning(self):
        logs = {(1,2) : "log1"}
        logbuff = LogBuffer(mock.Mock(iosize=2), logs)
        
        self.assertEquals(logbuff.getunallocated(), [(0, 1)])

    def test_getunallocated_WithTwoLogsTakingAllSpace_ReturnsEmpty(self):
        logs = {(0,1) : "log1", (1,2) : "log2"}
        logbuff = LogBuffer(mock.Mock(iosize=2), logs)
        
        self.assertEquals(logbuff.getunallocated(), [])

    def test_getunallocated_WithTwoLogsWithSpaceInbetween_ReturnsSpaceBetweenLogs(self):
        logs = {(0,1) : "log1", (2,3) : "log2"}
        logbuff = LogBuffer(mock.Mock(iosize=3), logs)
        
        self.assertEquals(logbuff.getunallocated(), [(1, 2)])

    def test_getunallocated_WithMultipleLogs_ReturnsSpaceBetweenLogs(self):
        logs = {(10,20) : "log1", (30,40) : "log2", (70,99) : "log3"}
        logbuff = LogBuffer(mock.Mock(iosize=100), logs)
        
        self.assertEquals(logbuff.getunallocated(), [(0, 10), (20, 30), (40, 70), (99, 100)])

    def test_FindEmptyLocation_CalledWithMultipleValues_ReturnsFirstLargeEnoughEntry(self):
        logs = {(1,2) : "log1", (4,5) : "log2", (8,10) : "log3"}
        logbuff = LogBuffer(mock.Mock(iosize=10), logs)
        self.assertEquals(logbuff.getunallocated(), [(0, 1), (2, 4), (5, 8)])

        self.assertEquals(logbuff.find_empty_location(1), 0)
        self.assertEquals(logbuff.find_empty_location(2), 2)
        self.assertEquals(logbuff.find_empty_location(3), 5)

    def test_load_WhenCalledWithLogIndexAndBufferReader_WriteLogsAreCorrectlyAssigned(self):
        logbuffer_reader = mock.Mock(read_entry = lambda pos: {0: ("log1", 1), 10: ("log2", 5)}[pos])
        logindex = mock.Mock(tocommit = [ LogIndexEntry(LogIndexEntry.WRITE, 0),
                                          LogIndexEntry(LogIndexEntry.WRITE, 10)])
        
        logbuff = LogBuffer.load(logindex, logbuffer_reader)
        
        self.assertEquals(logbuff.writelogs, 
                          {(0, 1) : "log1", (10, 15): "log2"})

class TestTransactional(unittest.TestCase):
    def test_1(self):
        IO_SIZE = 1000
        BUFFER_SIZE = 1000
        INDEX_COUNT = 20
        io = IoHandle.using_stringio(BUFFER_SIZE)
        buffer_reader = LogBufferReader(io, BUFFER_SIZE)
        logbuffer = LogBuffer(buffer_reader)
        
        io = IoHandle.using_stringio(LogIndexEntrySerializer.SERIALIZED_LENGTH * INDEX_COUNT)
        logindex_reader = LogIndexReader(io, INDEX_COUNT)
        logindex = SerializedLogIndex.new(logindex_reader)
        
        io = MultiChunkIO.using_stringios({0:IO_SIZE})
        log = TransactionLog(io, logindex, logbuffer)
        log.start_transaction()
        log.write(0, 3, "hello test")
        log.write(0, 12, "hello blog")

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
