# -*- coding:utf-8 -*-
"""
Created on 3 Jul 2011

@author: kris
"""
from coinpy.model.protocol.runmode import MAIN, TESTNET
from coinpy.model.protocol.structures.uint256 import uint256

COIN = 100000000
CENT = 1000000
MAX_MONEY = 21000000 * COIN

TARGET_TIMESPAN =  14 * 24 * 60 * 60 # 2 weeks
TARGET_SPACING = 10 * 60 # 10 minutes
TARGET_INTERVAL = TARGET_TIMESPAN / TARGET_SPACING #  2016 blocks / 2weeks

# block_time must be larger than the median of past "MEDIAN_TIME_SPAN" block_time's.
MEDIAN_TIME_SPAN=11

# when smaller, locktime is treated as a blockheight, otherwise as a blocktime
LOCKTIME_THRESHOLD = 500000000; # Tue Nov  5 00:53:20 1985 UTC


COINBASE_MATURITY=100
CONFIRMATIONS=6

MAX_BLOCK_SIZE = 1000000
#MAX_BLOCK_SIZE


PROOF_OF_WORK_LIMIT = {MAIN:     uint256.from_bignum((1 << (256 - 32)) - 1), #~uint256(0) >> 32
                       TESTNET : uint256.from_bignum((1 << (256 - 28)) - 1)} #~uint256(0) >> 28

def is_money_range(value):
    return (value >= 0 and value <= MAX_MONEY)
