# -*- coding:utf-8 -*-
"""
Created on 10 Jan 2012

@author: kris
"""
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.model.protocol.runmode import TESTNET, MAIN

BLOCKCHAIN_CHECKPOINTS_MAIN = \
{ 11111 :  Uint256.from_hexstr("0000000069e244f73d78e8fd29ba2fd2ed618bd6fa2ee92559f542fdb26e7c1d"),
  33333 :  Uint256.from_hexstr("000000002dd5588a74784eaa7ab0507a18ad16a236e7b1ce69f00d7ddfb5d0a6"),
  68555 :  Uint256.from_hexstr("00000000001e1b4903550a0b96e9a9405c8a95f387162e4944e8d9fbe501cd6a"),
  70567 :  Uint256.from_hexstr("00000000006a49b14bcf27462068f1264c961f11fa2e0eddd2be0791e1d4124a"),
  74000 :  Uint256.from_hexstr("0000000000573993a3c9e41ce34471c079dcf5f52a0e824a81e7f953b8661a20"),
 105000 :  Uint256.from_hexstr("00000000000291ce28027faea320c8d2b054b2e0fe44a773f3eefb151d6bdc97"),
 118000 :  Uint256.from_hexstr("000000000000774a7f8a7a12dc906ddb9e17e75d684f15e00f8767f9e8f36553"),
 134444 :  Uint256.from_hexstr("00000000000005b12ffd4cd315cd34ffd4a594f430ac814c91184a0d42d2b0fe"),
 140700 :  Uint256.from_hexstr("000000000000033b512028abb90e1626d8b346fd0ed598ac0a3c371138dce2bd")}

BLOCKCHAIN_CHECKPOINTS = {   MAIN    : BLOCKCHAIN_CHECKPOINTS_MAIN,
                             TESTNET : {} }

def verify_checkpoints(runmode, height, hash):
    checkpoints = BLOCKCHAIN_CHECKPOINTS[runmode]
    if (height in checkpoints):
        return (hash == checkpoints[height])
    return True
    
def get_checkpoint(runmode, height):
    checkpoints = BLOCKCHAIN_CHECKPOINTS[runmode]
    return (checkpoints[height])