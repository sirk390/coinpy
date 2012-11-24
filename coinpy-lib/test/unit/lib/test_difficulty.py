import unittest
from coinpy.lib.bitcoin.difficulty import uint256_difficulty, compact_difficulty
from coinpy.model.protocol.structures.uint256 import Uint256

class TestDifficulty(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_compact_difficulty(self):
        value = compact_difficulty(Uint256.from_bignum(0x00000000FFFF0000000000000000000000000000000000000000000000000000))
        assert value == 0x1d00ffff
        value = compact_difficulty(Uint256.from_bignum(0x00000000000404cb000000000000000000000000000000000000000000000000))
        assert value == 0x1b0404cb
        
    def test_uint256_difficulty(self):
        value = uint256_difficulty(0x1d00ffff)
        assert value == Uint256.from_bignum(0x00000000FFFF0000000000000000000000000000000000000000000000000000)
        value = uint256_difficulty(0x1b0404cb)
        assert value == Uint256.from_bignum(0x00000000000404cb000000000000000000000000000000000000000000000000)
        
if __name__ == '__main__':
    value = compact_difficulty(Uint256.from_bignum(0x00000000FFFF0000000000000000000000000000000000000000000000000000))
    #print value
    #print 0x1d00ffff
    unittest.main()
    
