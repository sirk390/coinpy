'''
    This module decodes data from a base58 plus 4 byte SHA256 checksum format.
    It is used in IRC bootstraping to encode the <IP+Port> of peers.     
'''

from base58 import b58decode, b58encode
import Crypto.Hash.SHA256 as SHA256
import Crypto.Hash.RIPEMD160 as RIPEMD160

def decode_base58check(data):
    raw = b58decode(data, None)
    if len(data) < 4:
        raise Exception("base58check: format error")
    content, check = raw[:-4], raw[-4:]
    digest1 = SHA256.new(content).digest()
    digest2 = SHA256.new(digest1).digest()
    if (digest2[:4] != check):
        print content, check, b58encode(digest2)
        raise Exception("base58check: checksum error %s != %s", (check, digest2))
    return (content)

def encode_base58check(content):
    digest1 = SHA256.new(content).digest()
    digest2 = SHA256.new(digest1).digest()
    return (b58encode(content + digest2[:4]))

