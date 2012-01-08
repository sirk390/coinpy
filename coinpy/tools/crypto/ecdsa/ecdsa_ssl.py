"""
[Simplified BSD, see http://www.opensource.org/licenses/bsd-license.html]

Copyright (c) 2011, Sam Rushing
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following disclaimer
      in the documentation and/or other materials provided with the
      distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import ctypes
import ctypes.util

# ctypes.util.find_library ('ssl')
# 
ssl = ctypes.cdll.LoadLibrary (ctypes.util.find_library ('libeay32'))

# this specifies the curve used with ECDSA.
NID_secp256k1 = 714 # from openssl/obj_mac.h

# Thx to Sam Devlin for the ctypes magic 64-bit fix.
def check_result (val, func, args):
    if val == 0:
        raise ValueError
    else:
        return ctypes.c_void_p (val)
ssl.EC_KEY_new_by_curve_name.restype = ctypes.c_void_p
ssl.EC_KEY_new_by_curve_name.errcheck = check_result

class KEY:
    def __init__ (self):
        self.k = ssl.EC_KEY_new_by_curve_name (NID_secp256k1)

    def __del__ (self):
        ssl.EC_KEY_free (self.k)
        self.k = None

    def generate (self):
        return ssl.EC_KEY_generate_key (self.k)

    def set_privkey (self, key):
        self.mb = ctypes.create_string_buffer (key)
        ssl.d2i_ECPrivateKey (ctypes.byref (self.k), ctypes.byref (ctypes.pointer (self.mb)), len(key))

    def set_pubkey (self, key):
        self.mb = ctypes.create_string_buffer (key)
        ssl.o2i_ECPublicKey (ctypes.byref (self.k), ctypes.byref (ctypes.pointer (self.mb)), len(key))

    def get_privkey (self):
        size = ssl.i2d_ECPrivateKey (self.k, 0)
        mb_pri = ctypes.create_string_buffer (size)
        ssl.i2d_ECPrivateKey (self.k, ctypes.byref (ctypes.pointer (mb_pri)))
        return mb_pri.raw

    def get_pubkey (self):
        size = ssl.i2o_ECPublicKey (self.k, 0)
        mb = ctypes.create_string_buffer (size)
        ssl.i2o_ECPublicKey (self.k, ctypes.byref (ctypes.pointer (mb)))
        return mb.raw

    def sign (self, hash):
        sig_size = ssl.ECDSA_size (self.k)
        mb_sig = ctypes.create_string_buffer (sig_size)
        sig_size0 = ctypes.POINTER (ctypes.c_int)()
        assert 1 == ssl.ECDSA_sign (0, hash, len (hash), mb_sig, ctypes.byref (sig_size0), self.k)
        return mb_sig.raw

    def verify (self, hash, sig):
        return ssl.ECDSA_verify (0, hash, len(hash), sig, len(sig), self.k)

if __name__ == '__main__':
    def hexstr(data):
        return ("".join("%02x" % ord(c) for c in data))
    
    key = KEY()
    key.generate()
    #print hexstr(key.get_privkey())
    
    key2 = KEY()
    key2.set_privkey(key.get_privkey())
    sig = key2.sign("oakzpodkpozakoda")
    print "sig", hexstr(sig)
    
    key3 = KEY()
    key3.set_pubkey(key.get_pubkey())
    print "sig", hexstr(key.get_pubkey())
    print "pubkey", key3.verify("oakzpodkpozakoda", sig)
    
    #sig: 3046022100bcddcd93b53cf9e95919e0e7bdd7dcbf0e86e2902c68de72b769bcfe6468c906022100fe4fd8eeb810a1a9cf547d99fe71768ad579bff16035e68690a1eca4ab9ab91401
    #pubkey:  048791c5168db93734e67f00a12560594cc9945c70862b55382774bbbd215e373ec6f48d956895adcb77b439d5a1baf82c0ae7b3924d56fbc7a7f4f3b41f65745f


    
    
