from coinpy.model.protocol.structures.uint256 import Uint256

def uint256_difficulty(bits):
    exp, value = bits >> 24, bits & 0xFFFFFF
    return (Uint256.from_bignum(value * 2 ** (8 * (exp - 3))))

def compact_difficulty(uin256):
    shr = 0
    bignumvalue = uin256.get_bignum()
    while ((bignumvalue >> (shr * 8)) > 0x7fffff):
        shr += 1
    exp, value = shr + 3, (bignumvalue >> (shr * 8) )
    return (exp << (3*8)| value)

if __name__ == "__main__":
    from coinpy.model.constants.bitcoin import PROOF_OF_WORK_LIMIT
    from coinpy.model.protocol.runmode import UNITNET, TESTNET, MAIN

    print compact_difficulty(PROOF_OF_WORK_LIMIT[UNITNET])
    print compact_difficulty(PROOF_OF_WORK_LIMIT[TESTNET])
    print compact_difficulty(PROOF_OF_WORK_LIMIT[MAIN])