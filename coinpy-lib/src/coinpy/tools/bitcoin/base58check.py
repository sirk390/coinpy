'''
    This module decodes data from a base58 plus 4 byte SHA256 checksum format.
    It is used in IRC bootstraping to encode the <IP+Port> of peers.     
'''

import Crypto.Hash.SHA256 as SHA256
from coinpy.tools.bitcoin.base256 import base256encode, base256decode
from coinpy.tools.bitcoin.base58 import base58decode, base58encode, b58chars,\
    count_leading_base58_zeros
from coinpy.tools.hex import hexstr
from coinpy.tools.bitcoin.sha256 import doublesha256

# Verify the checksum
def verify_base58check(data):
    try:
        decode_base58check(data)
    except:
        return False
    return True

# Verify the checksum + decode
def decode_base58check(data, preserve_leading_zeros=True):
    raw = preserve_leading_zeros and (count_leading_base58_zeros(data) * "\0") or ""
    raw += base256encode(base58decode(data))
    if len(raw) < 4:
        raise Exception("base58check: format error")
    content, check = raw[:-4], raw[-4:]
    digest2 = doublesha256(content)
    if (digest2[:4] != check):
        raise Exception("base58check: checksum error %s != %s" % (hexstr(digest2[:4]), hexstr(check)))
    return (content)

def encode_base58check(content, preserve_leading_zeros=True):
    """ Encode a bytestring (bid endian) as base58 with checksum.
     
        preserve_leading_zeros: argument used for MAIN bitcoin addresses (e.g.ADDRESSVERSION == 0)
        to preserve base256 leading zeros as base58 zeros ('1').
        For example:
            addrversion=00,hash160=00602005b16851c4f9d0e2c82fa161ac8190e04c will give the bitcoin address:
            112z9tWej11X94khKKzofFgWbdhiXLeHPD
    """
    digest1 = SHA256.new(content).digest()
    digest2 = SHA256.new(digest1).digest()
    data = content + digest2[:4]
    leading_zeros = None
    if preserve_leading_zeros:
        leading_zeros = 0
        while data[leading_zeros] == "\x00":
            leading_zeros += 1
    return (base58encode(base256decode(data), leading_zeros=leading_zeros))

