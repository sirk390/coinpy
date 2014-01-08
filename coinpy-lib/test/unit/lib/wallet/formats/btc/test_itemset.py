import unittest
from mock import Mock
from coinpy.lib.wallet.formats.btc.wallet_model import ItemSet, Transaction


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

    def test_ItemSet_deleteWithoutCommit_itemIsStillPresent(self):
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
        

    def test_ItemSet_OnChangingRaisesException_CommitIsNotDone(self):
        def onChangingCallback(change):
            raise Exception("error applying changes")
        itemset = ItemSet()
        itemset.ON_CHANGING.subscribe(onChangingCallback)

        itemset.begin_transaction()
        itemset.set("key1", 1)
        
        with self.assertRaises(Exception):
            itemset.commit_transaction()
        with self.assertRaises(KeyError):
            itemset.get("key1")

    def test_ItemSet_OnChangingEventRaisesException_CommitIsNotDone(self):
        def callback(change):
            raise Exception("error applying changes")
        itemset = ItemSet()
        itemset.ON_CHANGING.subscribe(callback)

        itemset.begin_transaction()
        itemset.set("key1", 1)
        
        with self.assertRaises(Exception):
            itemset.commit_transaction()
        with self.assertRaises(KeyError):
            itemset.get("key1")


    def test_ItemSet_Set2ItemSetsAndCommit_BothItemSetsAreSet(self):
        itemset1 = ItemSet()
        itemset2 = ItemSet()
        
        tx = Transaction()
        itemset1.set("testkey1", "value1", tx=tx)
        itemset2.set("testkey2", "value2", tx=tx)
        tx.commit()
        
        self.assertEquals(itemset1.get("testkey1"), "value1")
        self.assertEquals(itemset2.get("testkey2"), "value2")
        
    def test_ItemSet_SetPlusDeleteInDifferentItemSetsAndCommit_BothItemSetsAreUpdated(self):
        itemset1 = ItemSet()
        itemset2 = ItemSet({"testkey2" : "value2"})
        
        tx = Transaction()
        itemset1.set("testkey1", "value1", tx=tx)
        itemset2.delete("testkey2", tx=tx)
        tx.commit()
        
        self.assertEquals(itemset1.get("testkey1"), "value1")
        with self.assertRaises(KeyError):
            itemset2.get("testkey2")


if __name__ == '__main__':
    unittest.main()
    
