import unittest
import mock
from unit.parametrized_tests import UseParametrizedTests, testcases
from coinpy.lib.wallet.formats.btc.file_model import LogIndexEntry
from coinpy.lib.wallet.formats.btc.chunk_file import LogIndex,\
    CorruptLogIndexException, logindex_parse_groups, LogGroup, ATOMIC,\
    recover_logindex, TxLog

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


    def test_Recover_IncompleteTransactionWrittenToLogIndexEntry_TransactionIsErased(self):
        reader = makeLogIndexReader([LogIndexEntry(LogIndexEntry.BEGIN_TX, needs_commit=True),
                                     LogIndexEntry(LogIndexEntry.WRITE, argument=1, needs_commit=True)])
        
        recover_logindex(reader)
        
        reader.write_entry.assert_has_calls([ mock.call(1, LogIndexEntry(LogIndexEntry.WRITE, argument=1, needs_commit=False)),
                                              mock.call(0, LogIndexEntry(LogIndexEntry.BEGIN_TX, needs_commit=False)) ])

    def test_Recover_MoreThanThreeeUncommittedSequencesnLogIndexEntry_CallingRecoverRaisesException(self):
        reader = makeLogIndexReader([LogIndexEntry(LogIndexEntry.WRITE, needs_commit=False),
                                     LogIndexEntry(LogIndexEntry.WRITE, argument=2, needs_commit=True),
                                     LogIndexEntry(LogIndexEntry.WRITE, argument=2, needs_commit=False),
                                     LogIndexEntry(LogIndexEntry.WRITE, argument=2, needs_commit=True)])
        
        with self.assertRaises(CorruptLogIndexException):
            recover_logindex(reader)

class TestLogBuffer(unittest.TestCase):
    pass


        
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
"""
class WalletFile(object):
    def __init__(self, file_header, log_index_chunk, log_buffer_chunk, keys_chunk, outpoints_chunk, metadata_chunk):
        self.file_header = file_header
        self.log_index_chunk = log_index_chunk
        self.log_buffer_chunk = log_buffer_chunk"""
