from coinpy.tools.hex import decodehexstr
from coinpy.tools.hex import hexstr
from coinpy.model.wallet.masterkey import MasterKey
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.tools.crypto.ecdsa.ecdsa_ssl import KEY
import unittest
from coinpy.lib.wallet.bsddb.crypter.crypter import Crypter
from coinpy.lib.wallet.bsddb.crypter.passphrase import decrypt_masterkey


class TestWalletDatabase(unittest.TestCase):
    def setUp(self):
        pass
    def test_decrypt_private_key(self):
        master_key = MasterKey(crypted_key=decodehexstr("be4afa6923ad06790b0f8c3345131499cf2b149ca422bd11a7e67a76347c51a456a2d626f75da1ff809632fca7165d71"), 
                               salt=decodehexstr("8cdcbd8a494b0eeb"),
                               derivation_method=MasterKey.DERIVMETHOD_EVP_SHA512, 
                               derive_iterations=45193, other_derivation_parameters="")
        #Decrypt the master crypted_key using the passphrase
        plain_masterkey = decrypt_masterkey(master_key, "hello")
        print "plain_masterkey:", hexstr(plain_masterkey) 
        assert hexstr(plain_masterkey) == "56722b42c4b9f8689fe9b38745fe75af92d0a50d6fd94b34de6b6d5e287bbed3"
        #Decrypt a crypted_secret
        public_key = decodehexstr("046a82d73af2cc093e3df7ae0185f045946970bcd5f0ef26f82d4f9a24e0d50f977c51e311e079e3183cfadd67d9b3f089fe7ba94a196c365fbd9e03b8c423787d")
        crypted_secret = decodehexstr("ff914ab69f58af92ac56de85051441e729cc51e11608d563e2a266ce3b8c59f573ed6a1828ff98fadb345890b6ed2626")
        crypter2 = Crypter()
        crypter2.set_key(plain_masterkey, doublesha256(public_key))
        secret = crypter2.decrypt(crypted_secret)
        print "secret:", hexstr(secret) 
        assert hexstr(secret) == "1c7552a9b755d29d081efd71f7811cc8ab2c9f2c634f489e6b45700711c8a304"
        #Test the secret
        k = KEY()
        k.set_secret(secret)
        assert k.get_pubkey() == public_key
        sig1 = k.sign("sign something")
        k2 = KEY()
        k2.set_pubkey(public_key)
        assert k2.verify("sign something", sig1) == 1

if __name__ == '__main__':
    unittest.main()