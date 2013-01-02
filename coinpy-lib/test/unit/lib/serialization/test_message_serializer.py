import unittest
from coinpy.model.protocol.structures.invitem import INV_TX, Invitem, INV_BLOCK
from coinpy.model.protocol.messages.inv import InvMessage
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.lib.serialization.message_serializer import MessageSerializer
from coinpy.tools.hex import hexstr, decodehexstr
from coinpy.model.protocol.runmode import MAIN,TESTNET
from coinpy.lib.serialization.exceptions import FormatErrorException,\
    MissingDataException

class TestMessageSerializer(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_serialize_inv_message(self):
        inv_message = InvMessage([Invitem(INV_TX, Uint256.from_hexstr("f6eea3dd4f6536350344a535e37a4178170bba18b871a424d696e196d4d3b555")),
                                  Invitem(INV_BLOCK, Uint256.from_hexstr("0000000040a24e14497879bdd67db948cf30edc5d0a5833e8cb2736582157b49"))])
        serialized_msg = MessageSerializer(MAIN).serialize(inv_message)
        self.assertEquals(hexstr(serialized_msg), "f9beb4d9696e76000000000000000000490000008be920f5020100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")
        serialized_msg = MessageSerializer(TESTNET).serialize(inv_message)
        self.assertEquals(hexstr(serialized_msg), "fabfb5da696e76000000000000000000490000008be920f5020100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")

    def test_deserialize_inv_message(self):
        serialized_inv_message = decodehexstr("f9beb4d9696e76000000000000000000490000008be920f5020100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")
        inv_message, _ = MessageSerializer(MAIN).deserialize(serialized_inv_message)
        expected_message = InvMessage([Invitem(INV_TX, Uint256.from_hexstr("f6eea3dd4f6536350344a535e37a4178170bba18b871a424d696e196d4d3b555")),
                                       Invitem(INV_BLOCK, Uint256.from_hexstr("0000000040a24e14497879bdd67db948cf30edc5d0a5833e8cb2736582157b49"))])
        self.assertEquals(inv_message, expected_message)
        
    def test_deserialize_errors(self):
        # unknown command
        serialized_inv_message = decodehexstr("aabfb5da6c6e76000000000000000000490000008be920f5020100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")
        with self.assertRaises(FormatErrorException):
            inv_message, _ = MessageSerializer(TESTNET).deserialize(serialized_inv_message)
        # wrong magic (testnet magic on MAIN)
        serialized_inv_message = decodehexstr("fabfb5da696e76000000000000000000490000008be920f5020100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")
        with self.assertRaises(FormatErrorException):
            inv_message, _ = MessageSerializer(MAIN).deserialize(serialized_inv_message)
        # length field too large compared to data
        serialized_inv_message = decodehexstr("fabfb5da696e760000000000000000004A0000008be920f5020100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")
        with self.assertRaises(MissingDataException):
            inv_message, _ = MessageSerializer(TESTNET).deserialize(serialized_inv_message)
        # checksum error
        serialized_inv_message = decodehexstr("fabfb5da696e76000000000000000000490000008bf920f5020100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")
        with self.assertRaises(FormatErrorException):
            inv_message, _ = MessageSerializer(TESTNET).deserialize(serialized_inv_message)

if __name__ == '__main__':
    unittest.main()
    
