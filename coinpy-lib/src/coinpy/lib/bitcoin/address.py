# -*- coding:utf-8 -*-
"""
Created on 18 Feb 2012

@author: kris
"""
from coinpy.tools.bitcoin.hash160 import hash160
from coinpy.model.address_version import ADDRESSVERSION, ADDRESSVERSIONRUNMODE
from coinpy.tools.bitcoin.base58check import encode_base58check,\
    decode_base58check
from coinpy.model.protocol.runmode import RUNMODE_NAMES

class InvalidBitcoinAddress(Exception):
    pass

class BitcoinAddress():
    def __init__(self, hash160, runmode):
        self.hash160 = hash160 # bytestring of length 20
        self.runmode = runmode # MAIN / TESTNET
        
    @staticmethod
    def from_publickey(public_key, runmode):
        return BitcoinAddress(hash160(public_key), runmode)

    @staticmethod
    def from_base58addr(base58addrstr):
        try:
            data = decode_base58check(base58addrstr, 21)
        except Exception as e:
            raise InvalidBitcoinAddress("Unable to decode base58check : %s" % (str(e)))
        if (len(data) != 21):
            raise InvalidBitcoinAddress("BitcoinAddress.from_base58addr(): incorrect length")
        address_version, address = ord(data[0]), data[1:]
        return BitcoinAddress(address, ADDRESSVERSIONRUNMODE[address_version])
    
    def to_base58addr(self):
        return encode_base58check(chr(ADDRESSVERSION[self.runmode]) + self.hash160)
        
    def to_bytestring(self):
        return chr(ADDRESSVERSION[self.runmode]) + self.hash160
        
    @staticmethod
    def from_bytestring(bytestr):
        return BitcoinAddress(bytestr[1:], ADDRESSVERSIONRUNMODE[bytestr[0]])
    
    def get_hash160(self):
        return self.hash160
    
    def __str__(self):
        return "Address(%s,%s)" % (RUNMODE_NAMES[self.runmode], self.to_base58addr())
    
    def __hash__(self):
        return hash(self.hash160)
    
    def __eq__(self, other):
        return (self.runmode == other.runmode) and (self.hash160 == other.hash160)

    @staticmethod
    def is_valid(address_str, runmode):
        try:
            addr = BitcoinAddress.from_base58addr(address_str)
        except InvalidBitcoinAddress:
            return False
        return (addr.runmode == runmode)

if __name__ == '__main__':
    from coinpy.model.protocol.runmode import TESTNET, MAIN

    assert is_valid_bitcoin_address(TESTNET, "n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo")
    assert not is_valid_bitcoin_address(TESTNET, "n4NsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo")
    print is_valid_bitcoin_address(MAIN, "1H5azJoKoYd92DxjXX7k7gejpbLVMAczAi")    
    print is_valid_bitcoin_address(MAIN, "1H1hQVMZ6bpyGNWboJQT4aouDSksBnZWL3")
    print BitcoinAddress.from_base58addr("n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo")
    print BitcoinAddress.from_base58addr("1H5azJoKoYd92DxjXX7k7gejpbLVMAczAi")

