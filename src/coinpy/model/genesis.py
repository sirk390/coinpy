# -*- coding:utf-8 -*-
"""
Created on 7 Aug 2011

@author: kris
"""
from coinpy.model.protocol.structures.block import Block
from coinpy.model.protocol.structures.blockheader import BlockHeader
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.model.protocol.structures.tx_in import tx_in
from coinpy.model.protocol.structures.tx import tx
from coinpy.model.protocol.structures.outpoint import outpoint
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.opcodes import OP_PUSHDATA, OP_CHECKSIG
from coinpy.tools.hex import decodehexstr
from coinpy.model.scripts.script import Script
from coinpy.model.protocol.structures.tx_out import tx_out
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.lib.serialization.structures.s11n_blockheader import blockheader_serializer
from coinpy.model.protocol.runmode import MAIN, TESTNET

GENESIS_MAIN =  Block(
    BlockHeader(1, 
                uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), #hash_prev
                uint256.from_hexstr("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"), #merkle
                1231006505,  #time
                486604799,   #bits
                2083236893), #nonce
    [tx(1, #version
        [tx_in(outpoint(uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), 4294967295),     
               Script([Instruction(OP_PUSHDATA, decodehexstr("ffff001d")),Instruction(OP_PUSHDATA, decodehexstr("04")),Instruction(OP_PUSHDATA, "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks")]), #script
               4294967295) ], #inlist
        [tx_out(5000000000, #value
                Script([Instruction(OP_PUSHDATA, decodehexstr("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")),Instruction(OP_CHECKSIG)]))],
                0) #locktime         
     ])

GENESIS_TESTNET =  Block(
    BlockHeader(1, 
                uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), #hash_prev
                uint256.from_hexstr("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"), #merkle
                1296688602,  #time
                487063544,   #bits
                384568319), #nonce
    [tx(1, #version
        [tx_in(outpoint(uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), 4294967295),     
               Script([Instruction(OP_PUSHDATA, decodehexstr("ffff001d")),Instruction(OP_PUSHDATA, decodehexstr("04")),Instruction(OP_PUSHDATA, "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks")]), #script
               4294967295) ], #inlist
        [tx_out(5000000000, #value
                Script([Instruction(OP_PUSHDATA, decodehexstr("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")),Instruction(OP_CHECKSIG)]))],
                0) #locktime         
     ])

GENESIS = {MAIN : GENESIS_MAIN, TESTNET : GENESIS_TESTNET}

if __name__ == '__main__':
    from coinpy.lib.serialization.messages.s11n_block import block_encoder
    from coinpy.tools.hex import hexstr

    print GENESIS
    e = blockheader_serializer()
    print hexstr(e.encode(GENESIS.blockheader))
    print uint256.from_bytestr(doublesha256(e.encode(GENESIS.blockheader)))
    
    e = blockheader_serializer()
    print hexstr(e.encode(GENESIS_TESTNET.blockheader))
    print uint256.from_bytestr(doublesha256(e.encode(GENESIS_TESTNET.blockheader)))
    

