'''
    This module decodes data from a base58 plus 4 byte SHA256 checksum format.
    It is used in IRC bootstraping to encode the <IP+Port> of peers.     
'''

import Crypto.Hash.SHA256 as SHA256
from coinpy.tools.bitcoin.base256 import base256encode, base256decode
from coinpy.tools.bitcoin.base58 import base58decode, base58encode
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
def decode_base58check(data, pad=None):
    raw = base256encode(base58decode(data), pad and pad + 4)
    if len(raw) < 4:
        raise Exception("base58check: format error")
    content, check = raw[:-4], raw[-4:]
    digest2 = doublesha256(content)
    if (digest2[:4] != check):
        raise Exception("base58check: checksum error %s != %s" % (hexstr(digest2[:4]), hexstr(check)))
    return (content)

# Encode
def encode_base58check(content):
    digest1 = SHA256.new(content).digest()
    digest2 = SHA256.new(digest1).digest()
    return (base58encode(base256decode(content + digest2[:4])))

