from coinpy.model.protocol.structures.uint256 import Uint256

class BlockHeader():
    """A Blockheader defined in the bitcoin protocol.
        
        Attributes:
            version (int): Version number. 
            hash_prev (Uint256): Hash value of the previous block.
            hash_merkle Uint256: Hash of the transaction merkle tree.
            time (int): Unix timestamp in seconds.
            bits (int): Difficulty target. 
            nonce (int): Nonce.
    """
    def __init__(self, version, hash_prev, hash_merkle, time, bits, nonce):
        self.version, self.hash_prev, self.hash_merkle, self.time, self.bits, self.nonce = version, hash_prev, hash_merkle, time, bits, nonce
        # optional extra fields used to cache the hash value once computed
        self.hash = None
        self.rawdata = None

    def target(self):
        exp, value = self.bits >> 24, self.bits & 0xFFFFFF
        return Uint256.from_bignum(value * 2**(8*(exp - 3)))
                            
    def work(self):
        return ((1 << 256) / (self.target().get_bignum() + 1))
      
    def __eq__(self, other):
        return (self.version == other.version and 
                self.hash_prev == other.hash_prev and 
                self.hash_merkle == other.hash_merkle and 
                self.time == other.time and 
                self.bits == other.bits and 
                self.nonce == other.nonce)  
  
    def __str__(self):
        return ("BlockHeader(version:%d,hash_prev:%s,hash_merkle:%s,time:%d,bits:%d,nonce:%d)" % 
                    (self.version, 
                     self.hash_prev, 
                     self.hash_merkle, 
                     self.time,
                     self.bits,
                     self.nonce))
