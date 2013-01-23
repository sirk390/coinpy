import unittest
from coinpy.lib.transactions.address import BitcoinAddress,\
    InvalidBitcoinAddress
from coinpy.model.protocol.runmode import MAIN, TESTNET
from coinpy.tools.hex import hexstr, decodehexstr
from coinpy.model.address_version import PUBKEY_ADDRESS_MAIN,\
    PUBKEY_ADDRESS_TEST, AddressVersion, SCRIPT_ADDRESS_TEST,\
    SCRIPT_ADDRESS_MAIN

class TestBitcoinAddress(unittest.TestCase):
    def setUp(self):
        pass

    def test_address_from_public_key(self):
        """
        public: 023053536687205cbf57a25386ac466c7f85105032ced1ae9c54486a83c6dd3bab
        private: 049db42589b263e8700eb747a402b74604aae54ebc04f1cbe9a1cf584683f100
        """
        addr1 = BitcoinAddress.from_publickey(decodehexstr("023053536687205cbf57a25386ac466c7f85105032ced1ae9c54486a83c6dd3bab"), MAIN)
        self.assertEquals(addr1.to_base58addr(), "171waY81rzeFaBYhsiKibhBW5WAG8X7DLk")

    def test_address_from_bytestring(self):
        addr1 = BitcoinAddress.from_bytestring(decodehexstr("0041fe507633463c246ec91502c2d67e8b3d81618e"))
        self.assertEquals(addr1.to_base58addr(), "171waY81rzeFaBYhsiKibhBW5WAG8X7DLk")
        with self.assertRaises(InvalidBitcoinAddress):
            # not 21 characters
            addr2 = BitcoinAddress.from_bytestring(decodehexstr("0041fe507633463c246ec91502c2d67e8b3d81618e61"))
  
    def test_address_from_base58addr(self):
        #TESTNET 
        addr1 = BitcoinAddress.from_base58addr("n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo")
        self.assertEquals(hexstr(addr1.get_hash160()), 'fa92e151722c0ebca07059a505252218b4c50e7a')
        self.assertEquals(addr1.get_addr_version(), AddressVersion(PUBKEY_ADDRESS_TEST))
        #TESTNET script address
        addr2 = BitcoinAddress.from_base58addr("2NG68seqhTqLnniguW6efUDKyCHm4LYEFRa")
        self.assertEquals(hexstr(addr2.get_hash160()), 'fa92e151722c0ebca07059a505252218b4c50e7a')
        self.assertEquals(addr2.get_addr_version(), AddressVersion(SCRIPT_ADDRESS_TEST))
        #MAIN
        addr2 = BitcoinAddress.from_base58addr("1PqutNREJUX4VmMvhsNCRdymqRGAzifdsx")
        self.assertEquals(hexstr(addr2.get_hash160()), 'fa92e151722c0ebca07059a505252218b4c50e7a')
        self.assertEquals(addr2.get_addr_version(), AddressVersion(PUBKEY_ADDRESS_MAIN))
        #MAIN Script address
        addr2 = BitcoinAddress.from_base58addr("3QXvouufrNqSaw4Mpy2nrGLhywYtXx6wsi")
        self.assertEquals(hexstr(addr2.get_hash160()), 'fa92e151722c0ebca07059a505252218b4c50e7a')
        self.assertEquals(addr2.get_addr_version(), AddressVersion(SCRIPT_ADDRESS_MAIN))
        #TODO: MAIN with extra 1s

    def test_address_to_base58addr(self):
        self.assertEquals(BitcoinAddress(decodehexstr("b0600c55b16851c4f9d0e2c82fa161ac8190e04c"),
                                         AddressVersion(PUBKEY_ADDRESS_MAIN)).to_base58addr(),
                                        "1H5azJoKoYd92DxjXX7k7gejpbLVMAczAi")
    def test_address_to_bytestring(self):
        self.assertEquals(BitcoinAddress(decodehexstr("b0600c55b16851c4f9d0e2c82fa161ac8190e04c"),
                                         AddressVersion(PUBKEY_ADDRESS_MAIN)).to_bytestring(),
                                         decodehexstr("00b0600c55b16851c4f9d0e2c82fa161ac8190e04c"))
                          
    def test_address_to_hexstring(self):
        self.assertEquals(BitcoinAddress(decodehexstr("b0600c55b16851c4f9d0e2c82fa161ac8190e04c"),
                                         AddressVersion(PUBKEY_ADDRESS_MAIN)).to_hexstring(),
                                        "00b0600c55b16851c4f9d0e2c82fa161ac8190e04c")

    def test_address_get_hash160(self):
        self.assertEquals(BitcoinAddress(decodehexstr("b0600c55b16851c4f9d0e2c82fa161ac8190e04c"),
                                         AddressVersion(PUBKEY_ADDRESS_MAIN)).get_hash160(),
                                         decodehexstr("b0600c55b16851c4f9d0e2c82fa161ac8190e04c"))

    def test_address_get_addr_version(self):
        self.assertEquals(BitcoinAddress(decodehexstr("b0600c55b16851c4f9d0e2c82fa161ac8190e04c"),
                                         AddressVersion(PUBKEY_ADDRESS_TEST)).get_addr_version(),
                                         AddressVersion(PUBKEY_ADDRESS_TEST))

    def test_address_is_valid(self):
        assert BitcoinAddress.is_valid("2NG68seqhTqLnniguW6efUDKyCHm4LYEFRa", TESTNET) #script addr
        assert BitcoinAddress.is_valid("n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo", TESTNET) 
        assert BitcoinAddress.is_valid("112z9tWej11X94khKKzofFgWbdhiXLeHPD", MAIN)    
        assert BitcoinAddress.is_valid("3QXvouufrNqSaw4Mpy2nrGLhywYtXx6wsi", MAIN) #script addr 
        #checksum error
        assert not BitcoinAddress.is_valid("n4NsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo", TESTNET) 
        #invalid base64char l
        assert not BitcoinAddress.is_valid("n4lsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo", TESTNET) 
        # special case for MAIN, starting with multiple 1s 
        assert BitcoinAddress.is_valid("112z9tWej11X94khKKzofFgWbdhiXLeHPD", MAIN)    
        assert BitcoinAddress.is_valid("1111MJe7b4ZnktoPZabb6DLAKfac8tvx", MAIN)
        assert not BitcoinAddress.is_valid("11111MJe7b4ZnktoPZabb6DLAKfac8tvx", MAIN)
        assert not BitcoinAddress.is_valid("111MJe7b4ZnktoPZabb6DLAKfac8tvx", MAIN)

if __name__ == '__main__':
    unittest.main()
    
