# -*- coding:utf-8 -*-
"""
Created on 19 Apr 2012

@author: kris
"""
import ctypes
import ctypes.util

ssl = ctypes.cdll.LoadLibrary (ctypes.util.find_library ('libeay32'))

#EVP_BytesToKey(EVP_aes_256_cbc(), EVP_sha512()
"""
EVP_DecryptUpdate = ssl.EVP_DecryptUpdate
EVP_DecryptUpdate.argtypes = [ctypes.c_char_p, ctypes.POINTER]
"""