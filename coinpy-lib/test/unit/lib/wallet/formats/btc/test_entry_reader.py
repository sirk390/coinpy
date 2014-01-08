import unittest
from coinpy.lib.wallet.formats.btc.file_model import Alloc, Log
from coinpy.lib.wallet.formats.btc.entry_reader import FixedSizeEntryReader, AllocatedRange,\
    VarSizeEntryReader, InsufficientSpaceException
import mock
from unit.parametrized_tests import testcases, UseParametrizedTests
from coinpy.lib.wallet.formats.btc.file_handle import IoHandle
from coinpy.lib.wallet.formats.btc.serialization import LogSerializer

class TestLogIndexReader(unittest.TestCase):
    __metaclass__ = UseParametrizedTests

    @testcases([["entry1"], 
                ["entry2"]])
    def test_FixedSizeEntryReader_WriteEntry_EntryIsSerialized(self, entry):
        mockSerializer = mock.Mock(SERIALIZED_LENGTH = 1)
        reader = FixedSizeEntryReader(mock.Mock(), 1, serializer=mockSerializer)
        
        reader.write_entry(pos=0, entry=entry)
        
        mockSerializer.serialize.assert_called_once_with( entry)
        
    @testcases([["serialized1"], 
                ["serialized2"]])
    def test_FixedSizeEntryReader_WriteEntry_WriteSerializedEntryToIo(self, serialized_value):
        stubSerializer = mock.Mock(serialize = mock.Mock(return_value=serialized_value),
                                   SERIALIZED_LENGTH = 1)
        mockIo = mock.Mock()
        reader = FixedSizeEntryReader(mockIo, 1, serializer=stubSerializer)
        
        reader.write_entry(pos=0, entry="entry")
        
        mockIo.write.assert_called_once_with(0, serialized_value)

    @testcases([[1, 0, 0],
                [2, 1, 2],
                [2, 2, 4],])
    def test_FixedSizeEntryReader_WriteEntryAtPosition_WritesIoAtPositionMultipliedBySerializedSize(self, serialized_length, pos_written, expected_pos_written):
        stubSerializer = mock.Mock(serialize = mock.Mock(return_value="serialized"),
                                   SERIALIZED_LENGTH = serialized_length)
        mockIo = mock.Mock()
        reader = FixedSizeEntryReader(mockIo, pos_written+1, serializer=stubSerializer)
        
        reader.write_entry(pos=pos_written, entry="entry")
        
        mockIo.write.assert_called_once_with(expected_pos_written, "serialized")
        
    @testcases([[1], 
                [2]])
    def test_FixedSizeEntryReader_ReadEntry_ReadsSerializedSizeBytesFromIo(self, serialized_size):
        stubSerializer = mock.Mock(serialize = mock.Mock(return_value=serialized_size),
                                   SERIALIZED_LENGTH = serialized_size)
        mockIo = mock.Mock()
        reader = FixedSizeEntryReader(mockIo, 1, serializer=stubSerializer)
        
        reader.read_entry(pos=0)
        
        mockIo.read.assert_called_once_with(0, serialized_size)

class TestAllocatedRange(unittest.TestCase):
    def test_AllocatedRange_InsertDataAtPosition_GetAllocReturnsSplittedAllocs(self):
        r = AllocatedRange(io=mock.Mock(),
                           iosize=20,
                           serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.insert(0, data="abcde")
        
        self.assertEquals(r.getallocs(), [Alloc(empty=False, size=5), Alloc(empty=True, size=15)] )
        
    def test_AllocatedRange_AddDataTooLargeString_RaisesException(self):
        r = AllocatedRange(io=mock.Mock(),
                           iosize=17,
                           serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=2))
        
        with self.assertRaises(InsufficientSpaceException):
            r.add(data="onebytetoolong")
        
        

    def test_AllocatedRange_AddData_GetAllocReturnsSplittedAllocs(self):
        r = AllocatedRange(io=mock.Mock(),
                           iosize=20,
                           serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.add(data="abcde")
        
        self.assertEquals(r.getallocs(), [Alloc(empty=False, size=5), Alloc(empty=True, size=15)] )
        

    def test_AllocatedRange_RemoveMergeWithNext(self):
        r = AllocatedRange(io=mock.Mock(),
                           iosize=14,
                           allocs={0: Alloc(empty=False, size=3), 
                                   3: Alloc(empty=False, size=4), 
                                   7: Alloc(empty=True, size=7)}, 
                           serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.remove(3)
        
        self.assertEquals(r.getallocs(), [Alloc(empty=False, size=3), Alloc(empty=True, size=11)] )
        
    def test_AllocatedRange_RemoveMergeWithPrev(self):
        r = AllocatedRange(io=mock.Mock(),
                           iosize=14,
                           allocs={0: Alloc(empty=True, size=3), 
                                   3: Alloc(empty=False, size=4), 
                                   7: Alloc(empty=False, size=7)}, 
                           serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.remove(3)
        
        self.assertEquals(r.getallocs(), [Alloc(empty=True, size=7), Alloc(empty=False, size=7)] )
        
    def test_AllocatedRange_RemoveNoMerge(self):
        r = AllocatedRange(io=mock.Mock(),
                           iosize=14,
                           allocs={0: Alloc(empty=False, size=3), 
                                   3: Alloc(empty=False, size=4), 
                                   7: Alloc(empty=False, size=7)}, 
                           serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.remove(3)
        
        self.assertEquals(r.getallocs(), [Alloc(empty=False, size=3), Alloc(empty=True, size=4), Alloc(empty=False, size=7)] )
        
class TestVarSizeEntryReader(unittest.TestCase):
    def test_VarSizeEntryReader_AddTwoElementsRemoveFirstThenReRead_SecondElementIsReturned(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = VarSizeEntryReader(io, SIZE, LogSerializer, new=True)
 
        reader.add(Log(423, "hello", "world"))
        reader.add(Log(234, "aaa", "bbb")) 
        reader.remove(0)
        reader2 = VarSizeEntryReader(io, SIZE, LogSerializer)

        items = list(reader2.iteritems())
        self.assertEquals(items, [(23, Log(234, "aaa", "bbb"))])

    def test_VarSizeEntryReader_AddTwoElementsRemoveSecondThenReRead_FirstElementIsReturned(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = VarSizeEntryReader(io, SIZE, LogSerializer, new=True)
 
        reader.add(Log(423, "hello", "world"))
        pos2 = reader.add(Log(234, "aaa", "bbb")) 
        reader.remove(pos2)
        reader2 = VarSizeEntryReader(io, SIZE, LogSerializer)

        items = list(reader2.iteritems())
        self.assertEquals(items, [(0, Log(423, "hello", "world"))])

    def test_VarSizeEntryReader_AddThreeElementsRemoveSecondAndThirdThenReRead_FirstElementIsReturned(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = VarSizeEntryReader(io, SIZE, LogSerializer, new=True)
 
        reader.add(Log(423, "hello", "world"))
        pos2 = reader.add(Log(631, "x", "v"))
        pos3 = reader.add(Log(234, "aaa", "bbb")) 
        reader.remove(pos2)
        reader.remove(pos3)
        reader2 = VarSizeEntryReader(io, SIZE, LogSerializer)

        items = list(reader2.iteritems())
        self.assertEquals(items, [(0, Log(423, "hello", "world"))])

    def test_VarSizeEntryReader_AddThreeElementsRemoveFirstAndThirdThenReRead_SecondElementIsReturned(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = VarSizeEntryReader(io, SIZE, LogSerializer, new=True)
 
        pos1 = reader.add(Log(423, "hello", "world"))
        reader.add(Log(631, "x", "v"))
        pos3 = reader.add(Log(234, "aaa", "bbb")) 
        reader.remove(pos3)
        reader.remove(pos1)
        reader2 = VarSizeEntryReader(io, SIZE, LogSerializer)

        items = list(reader2.iteritems())
        self.assertEquals(items, [(23, Log(631, "x", "v"))])

    def test_VarSizeEntryReader_AddThreeElementsRemoveAll_CheckIOIsIdenticalToTheBeginning(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = VarSizeEntryReader(io, SIZE, LogSerializer, new=True)
        
        io1 = io.iohandle.getvalue()
        pos1 = reader.add(Log(423, "hello", "world"))
        pos2 = reader.add(Log(631, "x", "v"))
        pos3 = reader.add(Log(234, "aaa", "bbb")) 
        reader.remove(pos3)
        reader.remove(pos2)
        reader.remove(pos1)
        io2 = io.iohandle.getvalue()
        
        self.assertEquals(io1, io2)




        
    """def test_1(self):
        NB_ELEM = 10
        io = IoHandle.using_stringio(LogIndexEntrySerializer.SERIALIZED_LENGTH * NB_ELEM)
        reader = FixedSizeEntryReader(io, NB_ELEM, LogIndexEntrySerializer)
 
        for i in range(10):       
            reader.write_entry(i, LogIndexEntry(LogIndexEntry.WRITE, 0, needs_commit=False))
        reader.write_entry(0, LogIndexEntry(LogIndexEntry.WRITE, 0, needs_commit=True))
        reader.write_entry(1, LogIndexEntry(LogIndexEntry.BEGIN_TX, 3, needs_commit=True))

        print reader.read_entry(0)
        print reader.read_entry(1)


    def test_AllocatedRange_FillLargeEnoughEmptyLocation_GetHeadersAddEntry2(self):
        r = AllocatedRange(io=mock.Mock(),
                           space=[(None, 100)], 
                           header_serializer=mock.Mock(serialize=mock.Mock(return_value="-----"), SERIALIZED_LENGTH=5))
        
        r.insert(0, data="abcde")
        
        self.assertEquals(r.getspace(), [("abcde", 10), (None, 90)] )
    """
    """
    def test_VarSizeEntryReader_RemoveLastAddedElment_RestoresPreviousState(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = VarSizeEntryReader(io, SIZE, LogSerializer, new=True)
 
        reader.add(0, Log(423, "hello", "world"))
        v1 = io.iohandle.getvalue()
        reader.add(1, Log(234, "aaa", "bbb")) 
        reader.remove(1)
        v2 = io.iohandle.getvalue()
        
        self.assertEquals(v1, v2)
        #reader2 = VarSizeEntryReader(io, SIZE, LogSerializer)

    def test_VarSizeEntryReader_RemoveAndMergeWithNext_RestoresPreviousState(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = VarSizeEntryReader(io, SIZE, LogSerializer, new=True)
 
        reader.add(0, Log(423, "hello", "world"))
        v1 = io.iohandle.getvalue()
        reader.add(1, Log(324, "x", "y"))
        reader.add(2, Log(234, "aaa", "bbb")) 
        reader.remove(1)
        reader.remove(2)
        v2 = io.iohandle.getvalue()
        
        self.assertEquals(v1, v2)
    """
if __name__ == "__main__":
    unittest.main()
        