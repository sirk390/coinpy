import unittest
from coinpy.tools.ssl.ecdsa import KEY
from coinpy.tools.hex import decodehexstr, hexstr

class Test_SSL_ECDSA(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate(self):
        key = KEY()
        key.generate()
        sig = key.sign("cool")
        self.assertEquals(key.verify("cool", sig), 1)
        
    def test_set_privkey(self):
        key = KEY()
        key.set_privkey(decodehexstr("3081d3020101042030d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffba08185308182020101302c06072a8648ce3d0101022100fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f300604010004010704210279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798022100fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141020101a124032200030a43196c8bf389c0ce5987a3f4dac57f4ca0d9733c232659717d9404074b4504"))
        self.assertEquals(key.get_secret(),
                          decodehexstr("30d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffb"))

    def test_set_pubkey(self):
        sig = decodehexstr("3046022100b2a3e589f5ccd266b0b3ca34ec28a8730c34f16e7de2889f91fcb63824cb0da9022100b04e7b58680c55bb3cd5394c0feb5cfad98ba3695802e4fab61308f18d474031")
        key2 = KEY()
        key2.set_pubkey(decodehexstr("030a43196c8bf389c0ce5987a3f4dac57f4ca0d9733c232659717d9404074b4504"))
        self.assertEquals(key2.verify("cool", sig), 1)

    def test_ssl_get_privkey(self):
        key = KEY()
        key.set_secret(decodehexstr("30d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffb"), True)
        self.assertEquals(hexstr(key.get_privkey()), "3081d3020101042030d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffba08185308182020101302c06072a8648ce3d0101022100fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f300604010004010704210279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798022100fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141020101a124032200030a43196c8bf389c0ce5987a3f4dac57f4ca0d9733c232659717d9404074b4504")

    def test_ssl_get_secret(self):
        key = KEY()
        key.set_privkey(decodehexstr("3081d3020101042030d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffba08185308182020101302c06072a8648ce3d0101022100fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f300604010004010704210279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798022100fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141020101a124032200030a43196c8bf389c0ce5987a3f4dac57f4ca0d9733c232659717d9404074b4504"))
        self.assertEquals(hexstr(key.get_secret()), "30d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffb")
      
    def test_ssl_set_secret(self):
        key = KEY()
        key.set_secret(decodehexstr("30d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffb"), True)
        self.assertEquals(hexstr(key.get_privkey()), "3081d3020101042030d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffba08185308182020101302c06072a8648ce3d0101022100fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f300604010004010704210279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798022100fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141020101a124032200030a43196c8bf389c0ce5987a3f4dac57f4ca0d9733c232659717d9404074b4504")

    def test_ssl_get_pubkey(self):
        key = KEY()
        key.set_secret(decodehexstr("30d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffb"), True)
        self.assertEquals(hexstr(key.get_pubkey()), "030a43196c8bf389c0ce5987a3f4dac57f4ca0d9733c232659717d9404074b4504")

    def test_ssl_sign_verify(self):
        key = KEY()
        key.set_secret(decodehexstr("30d1d8d1d243ab41a80a3cc1481a626a137f771a636b2daca06c1f86cdfecffb"))
        sig = key.sign("cool")
        # verify on another key
        key2 = KEY()
        key2.set_pubkey(decodehexstr("030a43196c8bf389c0ce5987a3f4dac57f4ca0d9733c232659717d9404074b4504"))
        self.assertEquals(key2.verify("cool", sig), 1)
        self.assertEquals(key2.verify("coolx", sig), 0)
        self.assertEquals(key2.verify("cool", decodehexstr("3045022100ea3cbfca49123ecdcc419cf3277597307dca70b548ca1d4312f39186b043e86802201057af5c3889b65a59333d4f23bea915e76c2c26606dd35c57e00adf416ca31600")), 0)
    
    def tearDown(self):
        pass
    

if __name__ == '__main__':
    unittest.main()
    
