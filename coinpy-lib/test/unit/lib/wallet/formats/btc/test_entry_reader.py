import unittest
from coinpy.lib.wallet.formats.btc.file_model import ItemHeader, Log, LogHeader
from coinpy.lib.wallet.formats.btc.entry_reader import FixedSizeEntryReader, SerializedSet,\
    InsufficientSpaceException, LogBufferReader, SerializedDict
import mock
from unit.parametrized_tests import testcases, UseParametrizedTests
from coinpy.lib.wallet.formats.btc.file_handle import IoHandle
from coinpy.lib.wallet.formats.btc.serialization import LogHeaderSerializer

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

class TestSerializedSet(unittest.TestCase):
    
    def test_SerializedSet_InsertDataAtPosition_GetAllocReturnsSplittedAllocs(self):
        r = SerializedSet.new(io=mock.Mock(),
                               iosize=20,
                               serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.insert(0, data="abcde")
        
        self.assertEquals(r.getallocs(), [ItemHeader(empty=False, size=5), ItemHeader(empty=True, size=15)] )
        
    def test_SerializedSet_AddDataTooLargeString_RaisesException(self):
        r = SerializedSet.new(io=mock.Mock(),
                               iosize=17,
                               serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=2))
        
        with self.assertRaises(InsufficientSpaceException):
            r.add(data="onebytetoolong")
        
        

    def test_SerializedSet_AddData_GetAllocReturnsSplittedAllocs(self):
        r = SerializedSet.new(io=mock.Mock(),
                               iosize=20,
                               serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.add(data="abcde")
        
        self.assertEquals(r.getallocs(), [ItemHeader(empty=False, size=5), ItemHeader(empty=True, size=15)] )
        

    def test_SerializedSet_RemoveMergeWithNext(self):
        r = SerializedSet(io=mock.Mock(),
                           iosize=14,
                           allpos={0: ItemHeader(empty=False, size=3), 
                                   3: ItemHeader(empty=False, size=4), 
                                   7: ItemHeader(empty=True, size=7)}, 
                           serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.remove(3)
        
        self.assertEquals(r.getallocs(), [ItemHeader(empty=False, size=3), ItemHeader(empty=True, size=11)] )
        
    def test_SerializedSet_RemoveMergeWithPrev(self):
        r = SerializedSet(io=mock.Mock(),
                           iosize=14,
                           allpos={0: ItemHeader(empty=True, size=3), 
                                   3: ItemHeader(empty=False, size=4), 
                                   7: ItemHeader(empty=False, size=7)}, 
                           serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.remove(3)
        
        self.assertEquals(r.getallocs(), [ItemHeader(empty=True, size=7), ItemHeader(empty=False, size=7)] )
        
    def test_SerializedSet_RemoveNoMerge(self):
        r = SerializedSet(io=mock.Mock(),
                           iosize=14,
                           allpos={0: ItemHeader(empty=False, size=3), 
                                   3: ItemHeader(empty=False, size=4), 
                                   7: ItemHeader(empty=False, size=7)}, 
                           serializer=mock.Mock(serialize=mock.Mock(return_value=""), SERIALIZED_LENGTH=0))
        
        r.remove(3)
        
        self.assertEquals(r.getallocs(), [ItemHeader(empty=False, size=3), ItemHeader(empty=True, size=4), ItemHeader(empty=False, size=7)] )

    def test_SerializedSet_CreateNew_IterItemsIsEmpty(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = SerializedSet.new(io, SIZE)
 
        reader2 = SerializedSet.load(io, SIZE)

        items = list(reader2.itervalues())
        self.assertEquals(items, [])

    def test_SerializedSet_AddOneElements_CheckElementIsPresent(self):
        SIZE = 50
        io = IoHandle.using_stringio(SIZE)
        reader = SerializedSet.new(io, SIZE)
 
        reader.add("ab")
        
        #print repr(io.iohandle.getvalue())
        reader2 = SerializedSet.load(io, SIZE)

        items = list(reader2.itervalues())
        self.assertEquals(items, ["ab"])
        
    def test_SerializedSet_AddTwoElementsRemoveFirstThenReRead_SecondElementIsReturned(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = SerializedSet.new(io, SIZE)
 
        reader.add("abcd")
        reader.add("efghijkl") 
        reader.remove(0)
        reader2 = SerializedSet.load(io, SIZE)

        items = list(reader2.itervalues())
        self.assertEquals(items, ['efghijkl'])
        
    def test_SerializedSet_AddTwoElementsRemoveSecondThenReRead_FirstElementIsReturned(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = SerializedSet.new(io, SIZE)
 
        reader.add("abcd")
        pos2 = reader.add("efghijkl") 
        reader.remove(pos2)
        reader2 = SerializedSet.load(io, SIZE)

        items = list(reader2.itervalues())
        self.assertEquals(items, ["abcd"])
        
    def test_SerializedSet_AddThreeElementsRemoveSecondAndThirdThenReRead_FirstElementIsReturned(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = SerializedSet.new(io, SIZE)
 
        reader.add("abcd")
        pos2 = reader.add("efghijkl")
        pos3 = reader.add("mnopqrst") 
        reader.remove(pos2)
        reader.remove(pos3)
        reader2 = SerializedSet.load(io, SIZE)

        items = list(reader2.itervalues())
        self.assertEquals(items, ["abcd"])

    def test_SerializedSet_AddThreeElementsRemoveFirstAndThirdThenReRead_SecondElementIsReturned(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = SerializedSet.new(io, SIZE)
 
        pos1 = reader.add("abcd")
        reader.add("efghijkl")
        pos3 = reader.add("mnopqrst") 
        reader.remove(pos3)
        reader.remove(pos1)
        reader2 = SerializedSet.load(io, SIZE)

        items = list(reader2.itervalues())
        self.assertEquals(items, ["efghijkl"])

    def test_SerializedSet_AddThreeElementsRemoveAll_CheckIOIsIdenticalToTheBeginning(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = SerializedSet.new(io, SIZE)
        
        io1 = io.iohandle.getvalue()
        pos1 = reader.add("abcd")
        pos2 = reader.add("efghijkl")
        pos3 = reader.add("mnopqrst") 
        reader.remove(pos3)
        reader.remove(pos2)
        reader.remove(pos1)
        io2 = io.iohandle.getvalue()
        
        self.assertEquals(io1, io2)
        
class TestSerializedDict(unittest.TestCase):
    def test_SerializedDict_AddElementAndReload_DictIsTheSame(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        serialized_dict = SerializedDict.new(io, SIZE, LogHeaderSerializer)
        
        serialized_dict[4] = LogHeader(1, 32, 21)
        
        d2 = SerializedDict.load(io, SIZE, LogHeaderSerializer)
        self.assertEquals(list(d2.iteritems()), [(4, LogHeader(1, 32, 21))])

class TestLogBufferReader(unittest.TestCase):
    def test_LogBufferReader(self):
        SIZE = 1000
        io = IoHandle.using_stringio(SIZE)
        reader = LogBufferReader(io, SIZE)
 
        reader.write_entry(1, Log(LogHeader(5, 23123, 4), "abcd", "dcba"))

        self.assertEquals( reader.read_entry(1), (Log(LogHeader(5, 23123, 4), "abcd", "dcba"), 20))

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


    def test_SerializedSet_FillLargeEnoughEmptyLocation_GetHeadersAddEntry2(self):
        r = SerializedSet(io=mock.Mock(),
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
        