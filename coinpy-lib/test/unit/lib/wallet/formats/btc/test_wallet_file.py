import unittest
import mock
from coinpy.lib.wallet.formats.btc.file_handle import IoHandle
from coinpy.lib.wallet.formats.btc.serialization import LogIndexEntrySerializer
from coinpy.lib.wallet.formats.btc.entry_reader import LogBufferReader
from coinpy.lib.wallet.formats.btc.wallet_model import PubKeyOutpoint, PublicKey,\
    OutpointIndex
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.lib.wallet.formats.btc.wallet_file import WalletFile, TransactionalChunkFile
from io import SEEK_END, SEEK_SET




class TestWalletFile(unittest.TestCase):
    def test_WalletFile_1(self):
        
        io = IoHandle.using_stringio()
        wallet = WalletFile.new(io)
        wallet.start_tx()
        wallet.outpoints[1]= OutpointIndex(12, 
                                 Uint256.from_hexstr("2af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"),
                                 3,
                                 OutpointIndex.PUBKEY_HASH,
                                 4,
                                 PubKeyOutpoint(PublicKey.from_hexstr("022af4cc9ec3358354345c91691031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                                                is_pubkey_hash=True))
        wallet.end_tx()
        wallet.commit()
        wallet.start_tx()
        wallet.outpoints[1] = OutpointIndex(12, 
                                 Uint256.from_hexstr("2af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"),
                                 3,
                                 OutpointIndex.PUBKEY_HASH,
                                 4,
                                 PubKeyOutpoint(PublicKey.from_hexstr("022af4cc9ec3358354345c91691031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                                                is_pubkey_hash=True))
        wallet.end_tx()
        wallet.commit()

        #with open(r"c:\local\tmp\wallet-test.wlt", "wb") as wlt:
        #    wlt.write(io.iohandle.getvalue())
        io.seek(0, SEEK_SET)
        wallet2 = WalletFile.load(io, len(io.iohandle.getvalue()))
        
        print wallet2.fileheader
        print wallet2.outpoints
    '''
    def test_TransactionalChunkFile_2(self):
        w = TransactionalChunkFile()
    ''' 
        
        
if __name__ == "__main__":
    unittest.main()
