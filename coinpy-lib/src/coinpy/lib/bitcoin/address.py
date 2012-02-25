# -*- coding:utf-8 -*-
"""
Created on 18 Feb 2012

@author: kris
"""
from coinpy.tools.bitcoin.hash160 import hash160
from coinpy.model.address_version import ADDRESSVERSION
from coinpy.tools.bitcoin.base58check import encode_base58check

def get_address_from_public_key(runmode, public_key):
    return encode_base58check(chr(ADDRESSVERSION[runmode]) + hash160(public_key))

