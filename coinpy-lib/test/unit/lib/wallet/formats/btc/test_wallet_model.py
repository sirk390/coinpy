import unittest
import mock
from coinpy.lib.wallet.formats.btc.wallet_model import BtcWallet, PrivateKey,\
    PubKeyOutpoint, PublicKey, ItemSet

TEST_PRIVATEKEY = PrivateKey(0, private_key_data="\x01\x02\x03\x04" * 8)
TEST_OUTPOINT = PubKeyOutpoint(PublicKey.from_hexstr("01" * 33))



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
        wallet = BtcWallet()
        
        wallet.begin_transaction()
        wallet.private_keys.set(TEST_PRIVATEKEY.id, TEST_PRIVATEKEY)
        
        self.assertFalse(wallet.private_keys.contains(TEST_PRIVATEKEY.id))
        
    def test_WalletModel_AddPrivateKeyAndCommit_WalletContainsPrivateKey(self):
        wallet = BtcWallet()
        
        wallet.begin_transaction()
        wallet.private_keys.set(TEST_PRIVATEKEY.id, TEST_PRIVATEKEY)
        wallet.commit_transaction()
        
        self.assertEquals(wallet.private_keys.get(TEST_PRIVATEKEY.id), TEST_PRIVATEKEY)
        
    def test_WalletModel_AddBothPrivateKeyAndOutPointAndCommit_WalletContainsBoth(self):
        privkey = PrivateKey(0, private_key_data="\x01\x02\x03\x04" * 8)
        wallet = BtcWallet()
        
        wallet.begin_transaction()
        wallet.private_keys.set(TEST_PRIVATEKEY.id, TEST_PRIVATEKEY)
        wallet.outpoints.set(0, TEST_OUTPOINT)
        wallet.commit_transaction()
        
        self.assertEquals(wallet.private_keys.get(TEST_PRIVATEKEY.id), TEST_PRIVATEKEY)
        self.assertEquals(wallet.outpoints.get(0), TEST_OUTPOINT)
        
    def test_WalletModel_CommitPrivateKeyInTransactionResultsInError_BothPrivateKeyAndOutpointAreNotAdded(self):
        class TestException1(Exception):
            pass
        privkey = PrivateKey(0, private_key_data="\x01\x02\x03\x04" * 8)
        wallet = BtcWallet()
        wallet.private_keys.ON_CHANGING.subscribe(mock.Mock(side_effect=TestException1("Disk Error")))
        
        wallet.begin_transaction()
        wallet.private_keys.set(TEST_PRIVATEKEY.id, TEST_PRIVATEKEY)
        wallet.outpoints.set(0, TEST_OUTPOINT)
        with self.assertRaises(TestException1):
            wallet.commit_transaction()
        
        self.assertFalse(wallet.private_keys.contains(TEST_PRIVATEKEY.id))
        self.assertFalse(wallet.outpoints.contains(0))

    def test_WalletModel_CommitOutpointInTransactionResultsInError_BothPrivateKeyAndOutpointAreNotAdded(self):
        class TestException1(Exception):
            pass
        privkey = PrivateKey(0, private_key_data="\x01\x02\x03\x04" * 8)
        wallet = BtcWallet()
        wallet.outpoints.ON_CHANGING.subscribe(mock.Mock(side_effect=TestException1("Disk Error")))
        
        wallet.begin_transaction()
        wallet.private_keys.set(TEST_PRIVATEKEY.id, TEST_PRIVATEKEY)
        wallet.outpoints.set(0, TEST_OUTPOINT)
        with self.assertRaises(TestException1):
            wallet.commit_transaction()
        
        self.assertFalse(wallet.private_keys.contains(TEST_PRIVATEKEY.id))
        self.assertFalse(wallet.outpoints.contains(0))




        


if __name__ == '__main__':
    unittest.main()
    
