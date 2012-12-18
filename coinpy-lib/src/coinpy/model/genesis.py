from coinpy.model.protocol.structures.block import Block
from coinpy.model.protocol.structures.blockheader import BlockHeader
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.model.protocol.structures.tx_in import TxIn
from coinpy.model.protocol.structures.tx import Tx
from coinpy.model.protocol.structures.outpoint import Outpoint
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.opcodes import OP_PUSHDATA, OP_CHECKSIG
from coinpy.tools.hex import decodehexstr
from coinpy.model.scripts.script import Script
from coinpy.model.protocol.structures.tx_out import TxOut
from coinpy.model.protocol.runmode import MAIN, TESTNET, TESTNET3

GENESIS_MAIN =  Block(
    BlockHeader(1, 
                Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), #hash_prev
                Uint256.from_hexstr("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"), #merkle
                1231006505,  #time
                486604799,   #bits
                2083236893), #nonce
    [Tx(1, #version
        [TxIn(Outpoint(Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), 4294967295),     
                Script([Instruction(OP_PUSHDATA, decodehexstr("ffff001d")),Instruction(OP_PUSHDATA, decodehexstr("04")),Instruction(OP_PUSHDATA, "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks")]), #script
                4294967295) ], #inlist
        [TxOut(5000000000, #value
                Script([Instruction(OP_PUSHDATA, decodehexstr("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")),Instruction(OP_CHECKSIG)]))],
                0) #locktime         
     ])

GENESIS_TESTNET =  Block(
    BlockHeader(1, 
                Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), #hash_prev
                Uint256.from_hexstr("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"), #merkle
                1296688602,  #time
                487063544,   #bits
                384568319), #nonce
    [Tx(1, #version
        [TxIn(Outpoint(Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), 4294967295),     
                Script([Instruction(OP_PUSHDATA, decodehexstr("ffff001d")),Instruction(OP_PUSHDATA, decodehexstr("04")),Instruction(OP_PUSHDATA, "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks")]), #script
                4294967295) ], #inlist
        [TxOut(5000000000, #value
                Script([Instruction(OP_PUSHDATA, decodehexstr("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")),Instruction(OP_CHECKSIG)]))],
                0) #locktime         
     ])


GENESIS_TESTNET3 =  Block(
    BlockHeader(version=1, 
                hash_prev=Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), #hash_prev
                hash_merkle=Uint256.from_hexstr("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"), #merkle
                time=1296688602,  #time
                bits=486604799,   #bits
                nonce=414098458), #nonce
    [Tx(1, #version
        [TxIn(Outpoint(Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), 4294967295),     
                Script([Instruction(OP_PUSHDATA, decodehexstr("ffff001d")),Instruction(OP_PUSHDATA, decodehexstr("04")),Instruction(OP_PUSHDATA, "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks")]), #script
                4294967295) ], #inlist
        [TxOut(5000000000, #value
                Script([Instruction(OP_PUSHDATA, decodehexstr("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")),Instruction(OP_CHECKSIG)]))],
                0) #locktime         
     ])
GENESIS = {MAIN : GENESIS_MAIN, TESTNET : GENESIS_TESTNET, TESTNET3: GENESIS_TESTNET3}

if __name__ == '__main__':
    from coinpy.lib.blocks.hash_block import hash_block
    from coinpy.tools.hex import hexstr

    print GENESIS_MAIN
    print hash_block(GENESIS_MAIN)
    
    print GENESIS_TESTNET
    print hash_block(GENESIS_TESTNET)
    
    print GENESIS_TESTNET3
    print hash_block(GENESIS_TESTNET3)
    
