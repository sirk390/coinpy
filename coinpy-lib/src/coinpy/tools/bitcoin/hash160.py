import hashlib

def hash160(data):
    hash1 = hashlib.sha256(data).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hash1)
    return ripemd160.digest()
