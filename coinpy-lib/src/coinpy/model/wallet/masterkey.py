# -*- coding:utf-8 -*-
"""
Created on 19 Apr 2012

@author: kris
"""
from coinpy.tools.hex import hexstr

"""    MasterKey
 
    crypted_key:                  binstring
    salt:                         binstring
    derivation_method:            integer 0:EVP_sha512() 1: scrypt()
    derive_iterations:            integer, default=25000 (just under 0.1 seconds on a 1.86 GHz Pentium M)
    other_derivation_parameters:  binstring, additional derivation parameters 
    
    Example:

        master_key = MasterKey(crypted_key=decodehexstr("be4afa6923ad06790b0f8c3345131499cf2b149ca422bd11a7e67a76347c51a456a2d626f75da1ff809632fca7165d71"), 
                               salt=decodehexstr("8cdcbd8a494b0eeb"),
                               derivation_method=MasterKey.DERIVMETHOD_EVP_SHA512, 
                               derive_iterations=45193, "")
                               
       (passphrase is "hello")


    MasterKey holds a salt and random encryption key.
    
    MasterKey are encrypted using AES-256-CBC using a key
    derived using derivation method derivation_method and derive_iterations iterations.
    
    other_derivation_parameters is provided for alternative algorithms
    which may require more parameters (such as scrypt).
    
    Wallet Private Keys are then encrypted using AES-256-CBC
    with the double-sha256 of the public key as the IV, and the
    master key's key as the encryption key (see keystore.[ch]).
    
"""
class MasterKey():
    DERIVMETHOD_EVP_SHA512, DERIVMETHOD_SCRIPT = DERIVMETHODS = range(2)
    DERIVMETHODS_STR = {DERIVMETHOD_EVP_SHA512 : "EVP_sha512()", DERIVMETHOD_SCRIPT : "script()"}
    def __init__(self, 
                 crypted_key, 
                 salt, 
                 derivation_method, 
                 derive_iterations, 
                 other_derivation_parameters):
        self.crypted_key = crypted_key
        self.salt = salt
        self.derivation_method = derivation_method
        self.derive_iterations = derive_iterations
        self.other_derivation_parameters = other_derivation_parameters
    
    def __str__(self):
        return "MasterKey(crypted:%s, salt:%s, method:%s, iterations:%d)" % (
                                  hexstr(self.crypted_key), 
                                  hexstr(self.salt), 
                                  self.DERIVMETHODS_STR[self.derivation_method],
                                  self.derive_iterations)



