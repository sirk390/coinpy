from coinpy.lib.database.wallet.crypter.crypter import Crypter,\
    WALLET_CRYPTO_KEY_SIZE, WALLET_CRYPTO_SALT_SIZE
from coinpy.tools.crypto.ssl.ssl import ssl
import ctypes
from coinpy.tools.hex import hexstr
from coinpy.tools.crypto.random.random import Random
import time
from coinpy.model.wallet.masterkey import MasterKey

def derive_key_from_passphrase(passphrase, salt, derive_iterations, deriv_method):
    """Derive (key, initialization_vector) from passphrase and derivation parameters"""
    passphrase = passphrase.encode("utf-8")
    chKey = ctypes.create_string_buffer (WALLET_CRYPTO_KEY_SIZE)
    chIV = ctypes.create_string_buffer (WALLET_CRYPTO_KEY_SIZE)
    if len(salt) != WALLET_CRYPTO_SALT_SIZE:
        raise Exception("Error in salt size. found:%d, expected:%d" % (len(salt), WALLET_CRYPTO_SALT_SIZE))
    i = ssl.EVP_BytesToKey(ssl.EVP_aes_256_cbc(), ssl.EVP_sha512(), 
                       salt, passphrase, 
                       len(passphrase), derive_iterations, chKey, chIV)
    if i != WALLET_CRYPTO_KEY_SIZE:
        raise Exception("Error decrypting masterkey: EVP_BytesToKey")
    return (chKey, chIV)

def decrypt_masterkey(master_key, passphrase):
    """Return plain master key bytestring from a MasterKey object and a passphrase"""
    key, init_vect = derive_key_from_passphrase(passphrase, master_key.salt,  master_key.derive_iterations, master_key.derivation_method)
    crypter = Crypter()
    crypter.set_key(key, init_vect)
    plain_masterkey = crypter.decrypt(master_key.crypted_key)
    return plain_masterkey


def new_masterkey(passphrase):
    """Create a new masterkey"""
    rand = Random()
    crypter = Crypter()
    plain_master_key = rand.get_random_bytes(WALLET_CRYPTO_KEY_SIZE)
    rand.add_system_seeds()
    salt = rand.get_random_bytes(WALLET_CRYPTO_SALT_SIZE)
    deriv_method = MasterKey.DERIVMETHOD_EVP_SHA512
    
    target_seconds = 0.1 #100ms
    # estimate number of derivations for 100ms per decrypt using 25000 iterations.
    start_time = time.time()
    derive_key_from_passphrase(passphrase, salt, 25000, deriv_method)
    estimate1 = int((25000.0 * target_seconds) / (time.time() - start_time))
    # try it and take the mean of the estimate1 and estimate2
    start_time = time.time()
    derive_key_from_passphrase(passphrase, salt, estimate1, deriv_method)
    estimate2 = int(estimate1 * target_seconds / (time.time() - start_time))
    deriv_iterations = (estimate1 + estimate2) / 2
    # use it
    key, init_vect = derive_key_from_passphrase(passphrase, salt, deriv_iterations, deriv_method)
    crypter.set_key(key, init_vect)
    crypted_key = crypter.encrypt(plain_master_key)
    return MasterKey(crypted_key, salt, deriv_method, deriv_iterations)

if __name__ == '__main__':
    from coinpy.tools.hex import decodehexstr
    from coinpy.tools.hex import hexstr
    from coinpy.model.wallet.masterkey import MasterKey
    from coinpy.tools.bitcoin.sha256 import doublesha256
    from coinpy.tools.crypto.ecdsa.ecdsa_ssl import KEY

    master_key = MasterKey(crypted_key=decodehexstr("be4afa6923ad06790b0f8c3345131499cf2b149ca422bd11a7e67a76347c51a456a2d626f75da1ff809632fca7165d71"), 
                           salt=decodehexstr("8cdcbd8a494b0eeb"),
                           derivation_method=MasterKey.DERIVMETHOD_EVP_SHA512, 
                           derive_iterations=45193, other_derivation_parameters="")
    #Decrypt the master crypted_key using the passphrase
    plain_masterkey = decrypt_masterkey(master_key, "hello")
    #Decrypt a crypted_secret
    public_key = decodehexstr("046a82d73af2cc093e3df7ae0185f045946970bcd5f0ef26f82d4f9a24e0d50f977c51e311e079e3183cfadd67d9b3f089fe7ba94a196c365fbd9e03b8c423787d")
    crypted_secret = decodehexstr("ff914ab69f58af92ac56de85051441e729cc51e11608d563e2a266ce3b8c59f573ed6a1828ff98fadb345890b6ed2626")
    crypter2 = Crypter()
    crypter2.set_key(plain_masterkey, doublesha256(public_key))
    secret = crypter2.decrypt(crypted_secret)
    print hexstr(secret)
    #Test the secret
    k = KEY()
    k.set_secret(secret)
    sig = signature1 = k.sign("sign something")
    k2 = KEY()
    k2.set_pubkey(public_key)
    print k2.verify("sign something", sig)
    
    #Create a new masterkey
    m =  new_masterkey("hello hello")
    print m
    print hexstr(decrypt_masterkey(m, "hello hello" ))
        
