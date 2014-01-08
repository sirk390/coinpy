import unittest
import mock
from coinpy.lib.wallet.formats.btc.wallet_model import BtcWallet, PrivateKey,\
    PubKeyOutpoint, PublicKey

TEST_PRIVATEKEY = PrivateKey(0, private_key_data="\x01\x02\x03\x04" * 8)
TEST_OUTPOINT = PubKeyOutpoint(PublicKey.from_hexstr("01" * 33))

class TestWalletModel1(unittest.TestCase):
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
    
