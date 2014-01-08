import unittest
from mock import Mock
from coinpy.lib.wallet.formats.btc.wallet_model import BtcWallet, PrivateKey,\
    ItemSet,  Transaction
import StringIO
from coinpy.lib.wallet.formats.btc.file_model import FileHeader, ChunkHeader, MetadataChunk, LogIndexChunk, LogBufferChunk, KeysChunk,\
    OutpointsChunk, WalletFile, Metadata



class TestItemSet(unittest.TestCase):
    def test_ItemSet_setAndCommit_getReturnsValue(self):
        items = ItemSet()
        items.begin_transaction()
        items.set("key1", 1)
        items.commit_transaction()
        
        self.assertEquals(items.get("key1"), 1)
        
    def test_ItemSet_setWithoutCommit_getThrowsKeyError(self):
        items = ItemSet()
        items.begin_transaction()
        items.set("key1", 1)
        
        with self.assertRaises(KeyError):
            print items.get("key1")

    def test_ItemSet_delete_itemIsStillPresent(self):
        items = ItemSet({"key1" : 1})
        items.begin_transaction()
        items.delete("key1")
        
        self.assertEquals(items.get("key1"), 1)
 
    def test_ItemSet_deleteAndCommit_itemIsDeleted(self):
        items = ItemSet({"key1" : 1})
        items.begin_transaction()
        items.delete("key1")
        items.commit_transaction()
         
        with self.assertRaises(KeyError):
            items.get("key1")

    def test_ItemSet_deleteTwice_raisesKeyError(self):
        items = ItemSet({"key1" : 1})
        items.begin_transaction()
        items.delete("key1")
         
        with self.assertRaises(KeyError):
            items.delete("key1")

    def test_ItemSet_deleteNotPresentItem_raisesKeyError(self):
        items = ItemSet()
        items.begin_transaction()
         
        with self.assertRaises(KeyError):
            items.delete("key1")
            
    def test_ItemSet_setTwice_getReturnsSecondValue(self):
        items = ItemSet()
        
        items.begin_transaction()
        items.set("key1", 1)
        items.set("key1", 2)
        items.commit_transaction()
        
        self.assertEquals(items.get("key1"), 2)

    def test_ItemSet_setAndDelete_getRaisesKeyError(self):
        items = ItemSet()
        
        items.begin_transaction()
        items.set("key1", 1)
        items.delete("key1")
        items.commit_transaction()
        
        with self.assertRaises(KeyError):
            items.get("key1")
        


class TestWalletModel(unittest.TestCase):

    def test_WalletModel_AddPrivateKey_WalletDoesNotYetContainPrivateKey(self):
        privkey = PrivateKey(0, private_key_data="\x01\x02\x03\x04" * 8)
        wallet = BtcWallet()
        wallet.begin_transaction()
        wallet.private_keys.set(privkey.id, privkey)
        
        self.assertFalse(wallet.private_keys.contains(privkey.id))
        
    def test_WalletModel_AddPrivateKeyAndCommit_WalletContainsPrivateKey(self):
        privkey = PrivateKey(0, private_key_data="\x01\x02\x03\x04" * 8)
        wallet = BtcWallet()
        wallet.begin_transaction()
        wallet.private_keys.set(privkey.id, privkey)
        
        wallet.commit_transaction()
        
        self.assertEquals(wallet.private_keys.get(privkey.id), privkey)

if __name__ == '__main__':
    unittest.main()
    
