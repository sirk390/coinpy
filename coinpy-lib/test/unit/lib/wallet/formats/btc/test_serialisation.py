import unittest
from coinpy.lib.wallet.formats.btc.file_model import ChunkHeader,\
    ItemHeader, LogIndexEntry
from coinpy.lib.wallet.formats.btc.serialization import DeserializationException, ChunkHeaderSerializer, PubKeyOutpointSerializer,\
    MultiSigOutpointSerializer, OutpointIndexSerializer, ItemHeaderSerializer,\
    LogIndexEntrySerializer
from coinpy.tools.hex import decodehexstr, hexstr
from coinpy.lib.wallet.formats.btc.wallet_model import PubKeyOutpoint, PublicKey,\
    OutpointIndex, MultiSigOutpoint
from coinpy.model.protocol.structures.uint256 import Uint256

class TestWalletSerialization(unittest.TestCase):
    def test_serialize_logindex_begin_tx(self):
        log_index = LogIndexEntry(LogIndexEntry.BEGIN_TX, needs_commit=True)
        
        serialized = LogIndexEntrySerializer.serialize(log_index)

        self.assertEquals(serialized, 
                          decodehexstr("010000000001"))

    def test_serialize_logindex_end_tx(self):
        log_index = LogIndexEntry(LogIndexEntry.END_TX, needs_commit=False)
        
        serialized = LogIndexEntrySerializer.serialize(log_index)

        self.assertEquals(serialized, 
                          decodehexstr("020000000000"))

    def test_serialize_logindex_write(self):
        log_index = LogIndexEntry(LogIndexEntry.WRITE, 34234242, needs_commit=True)
        
        serialized = LogIndexEntrySerializer.serialize(log_index)

        self.assertEquals(serialized, 
                          decodehexstr("03020a5f8201"))

    def test_deserialize_logindex_begin_tx(self):
        log_index = LogIndexEntrySerializer.deserialize(decodehexstr("010000000001"))

        self.assertEquals(log_index, 
                          LogIndexEntry(LogIndexEntry.BEGIN_TX, needs_commit=True))

    def test_deserialize_logindex_end_tx(self):
        log_index = LogIndexEntrySerializer.deserialize(decodehexstr("020000000000"))

        self.assertEquals(log_index, 
                          LogIndexEntry(LogIndexEntry.END_TX, needs_commit=False))

    def test_deserialize_logindex_write(self):
        log_index = LogIndexEntrySerializer.deserialize(decodehexstr("03020a5f8201"))

        self.assertEquals(log_index, 
                          LogIndexEntry(LogIndexEntry.WRITE, 34234242, needs_commit=True))

    def test_deserialize_error_length(self):
        data1 = decodehexstr("032422")
        data2 = decodehexstr("032422032422032422032422")
        
        with self.assertRaises(DeserializationException):
            LogIndexEntrySerializer.deserialize(data1)
        with self.assertRaises(DeserializationException):
            LogIndexEntrySerializer.deserialize(data2)


    def test_serialize_chunk_header(self):
        chunkheader = ChunkHeader("name", 23324432, 87312313, 478498)
        
        serialized = ChunkHeaderSerializer.serialize(chunkheader)

        self.assertEquals(hexstr(serialized), 
                          "6e616d650163e710053447b900074d22")

    def test_deserialize_chunk_header(self):
        data = decodehexstr("6e616d650163e710053447b900074d22")
        
        deserialized = ChunkHeaderSerializer.deserialize(data)

        self.assertEquals(deserialized, 
                          ChunkHeader("name", 23324432, 87312313, 478498))


    # Wallet serialisation
    def test_serialize_pubkey_outpoint(self):
        pubkey_outpoint = PubKeyOutpoint(PublicKey.from_hexstr("022af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                         is_pubkey_hash=True)
        
        serialized = PubKeyOutpointSerializer.serialize(pubkey_outpoint)

        self.assertEquals(hexstr(serialized), 
                          "022af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f")

    def test_deserialize_pubkey_outpoint(self):
        serialized_data = decodehexstr("022af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f")
        
        pubkey_outpoint = PubKeyOutpointSerializer.deserialize(serialized_data, 
                                                               outpoint_type=OutpointIndex.PUBKEY)

        self.assertEquals(pubkey_outpoint, 
                          PubKeyOutpoint(PublicKey.from_hexstr("022af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                                                is_pubkey_hash=False))

    def test_serialize_multisig_outpoint(self):
        outpoint = MultiSigOutpoint(2, 3,
                                    [PublicKey.from_hexstr("022af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                     PublicKey.from_hexstr("022dc45c9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                     PublicKey.from_hexstr("029ce0129ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f")])
        
        serialized = MultiSigOutpointSerializer.serialize(outpoint)

        self.assertEquals(hexstr(serialized), 
                          "0000000200000003022af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f022dc45c9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f029ce0129ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f")

    def test_deserialize_multisig_outpoint(self):
        serialized_data = decodehexstr("0000000200000003022af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f022dc45c9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f029ce0129ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f")
        
        outpoint = MultiSigOutpointSerializer.deserialize(serialized_data)

        self.assertEquals(outpoint, 
                          MultiSigOutpoint(2, 3,
                                    [PublicKey.from_hexstr("022af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                     PublicKey.from_hexstr("022dc45c9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                     PublicKey.from_hexstr("029ce0129ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f")])
                          )

    def test_serialize_outpoint_index(self):
        outpoint = OutpointIndex(12, 
                                 Uint256.from_hexstr("2af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"),
                                 3,
                                 OutpointIndex.PUBKEY_HASH,
                                 4,
                                 PubKeyOutpoint(PublicKey.from_hexstr("022af4cc9ec3358354345c91691031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                                                is_pubkey_hash=True))
        serialized = OutpointIndexSerializer.serialize(outpoint)

        self.assertEquals(hexstr(serialized), 
                          "0000000c2af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f030200000004022af4cc9ec3358354345c91691031a1fcdbe9a9064197521814e8a20fe018eb5f")

    def test_deserialize_outpoint_index(self):
        serialized_data = decodehexstr("0000000c2af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f030200000004022af4cc9ec3358354345c91691031a1fcdbe9a9064197521814e8a20fe018eb5f")
        
        outpoint_index = OutpointIndexSerializer.deserialize(serialized_data)

        self.assertEquals(outpoint_index, 
                          OutpointIndex(12, 
                                 Uint256.from_hexstr("2af4cc9ec3358354345c91694031a1fcdbe9a9064197521814e8a20fe018eb5f"),
                                 3,
                                 OutpointIndex.PUBKEY_HASH,
                                 4,
                                 PubKeyOutpoint(PublicKey.from_hexstr("022af4cc9ec3358354345c91691031a1fcdbe9a9064197521814e8a20fe018eb5f"), 
                                                                is_pubkey_hash=True))
                          )

    def test_serialize_NotEmptyItemHeader_HexValueIsCorrect(self):
        item_header = ItemHeader(empty=False, id=0x43ecda, size=0xec39a0)
        
        serialized = ItemHeaderSerializer.serialize(item_header)

        self.assertEquals(hexstr(serialized), "01" "0043ecda" "00ec39a0")

    def test_serialize_EmptyItemHeader_HexValueIsCorrect(self):
        item_header = ItemHeader(empty=True, id=0x12ecda, size=0xdc39a0)
        
        serialized = ItemHeaderSerializer.serialize(item_header)

        self.assertEquals(hexstr(serialized), "00" "0012ecda" "00dc39a0")






    
if __name__ == '__main__':
    unittest.main()
    
