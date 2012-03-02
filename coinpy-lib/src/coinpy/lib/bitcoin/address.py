# -*- coding:utf-8 -*-
"""
Created on 18 Feb 2012

@author: kris
"""
from coinpy.tools.bitcoin.hash160 import hash160
from coinpy.model.address_version import ADDRESSVERSION
from coinpy.tools.bitcoin.base58check import encode_base58check,\
    decode_base58check

def get_address_from_public_key(runmode, public_key):
    return encode_base58check(chr(ADDRESSVERSION[runmode]) + hash160(public_key))


def is_valid_bitcoin_address(runmode, address_str):
    try:
        data = decode_base58check(address_str)
    except:
        return False
    if (len(data) != 21):
        return False
    address_version, address = ord(data[0]), data[1:]
    return ADDRESSVERSION[runmode] == address_version

if __name__ == '__main__':
    from coinpy.model.protocol.runmode import TESTNET

    assert is_valid_bitcoin_address(TESTNET, "n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo")
    assert not is_valid_bitcoin_address(TESTNET, "n4NsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo")
    