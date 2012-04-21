# -*- coding:utf-8 -*-
"""
Created on 19 Apr 2012

@author: kris
"""
import ctypes
from coinpy.tools.crypto.ssl.ssl import ssl

WALLET_CRYPTO_KEY_SIZE = 32
WALLET_CRYPTO_SALT_SIZE = 8

class Crypter():
    def __init__(self):
        self.chKey = ctypes.create_string_buffer (WALLET_CRYPTO_KEY_SIZE)
        self.chIV = ctypes.create_string_buffer (WALLET_CRYPTO_KEY_SIZE)
    
    def set_key(self, key, init_vect):
        self.key = key
        self.init_vect = init_vect
    
    def decrypt(self, crypted_data):
        # plaintext will always be equal to or lesser than length of ciphertext
        l = len(crypted_data)
        plain_text = ctypes.create_string_buffer (l)
        ctx = ssl.EVP_CIPHER_CTX_new()
        ssl.EVP_CIPHER_CTX_init(ctx);
        ssl.EVP_DecryptInit_ex(ctx, ssl.EVP_aes_256_cbc(), 0, self.key, self.init_vect);
        len1 = ctypes.c_int()
        len2 = ctypes.c_int()
        ssl.EVP_DecryptUpdate(ctx, plain_text, ctypes.byref (len1), crypted_data, l)
        ssl.EVP_DecryptFinal_ex(ctx, ctypes.addressof(plain_text) + len1.value, ctypes.byref(len2))
        ssl.EVP_CIPHER_CTX_cleanup(ctx);
        #todo: free ctx
        return plain_text.raw[:len1.value+len2.value]

    