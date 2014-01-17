import unittest
import StringIO
from coinpy.lib.wallet.formats.btc.file_handle import IoHandle


class Test(unittest.TestCase):
    def test_RandomAccessIoHandle_WriteDataAtPosition2_DataIsWritten(self):
        io = StringIO.StringIO("0123456789")
        handle = IoHandle(io)
        
        handle.write(2, "--")

        self.assertEquals(io.getvalue(), "01--456789")

    def test_RandomAccessIoHandle_ReadDataAtPosition3_DataIsReturned(self):
        io = StringIO.StringIO("0123456789")
        handle = IoHandle(io)
        
        result = handle.read(offset=2, length=3)

        self.assertEquals(result, "234")
    
if __name__ == "__main__":
    unittest.main()