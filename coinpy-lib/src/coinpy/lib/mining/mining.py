from coinpy.model.protocol.structures.block import Block
from coinpy.model.protocol.structures.blockheader import BlockHeader
from coinpy.lib.transactions.merkle_tree import compute_merkle_root
from coinpy.model.protocol.structures.tx import Tx
from coinpy.model.protocol.structures.tx_out import TxOut
from coinpy.model.protocol.structures.tx_in import TxIn
from coinpy.model.protocol.structures.outpoint import Outpoint
from coinpy.model.scripts.script import RawScript, Script
from coinpy.lib.blocks.hash_block import hash_blockheader
from coinpy.lib.serialization.structures.s11n_blockheader import BlockheaderSerializer
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.model.constants.bitcoin import PROOF_OF_WORK_LIMIT
from coinpy.lib.blocks.difficulty import uint256_difficulty
import collections
from coinpy.lib.time.time_source import SystemTimeSource
from coinpy.tools.bitcoin.base256 import base256encode
from coinpy.tools.hex import hexstr
from coinpy.lib.serialization.scripts.serialize import IntructionSerializer,\
    ScriptSerializer
from coinpy.lib.vm.script.push_data import push_bignum_instruction,\
    push_data_instruction

class BlockheaderTemplate():
    def __init__(self, 
                 hash_prev, 
                 block_height, # version 2 blocks see BIP-34
                 coinbase_txout_list, 
                 transactions, 
                 time, 
                 bits,
                 nonce=0,
                 extra_nonce=0,
                 coinbase_flags=["/P2SH/"]):
        self.nonce = nonce
        self.extra_nonce = extra_nonce
        self.hash_prev = hash_prev
        self.block_height = block_height
        self.coinbase_txout_list = coinbase_txout_list
        self.transactions = transactions
        self.time = time
        self.bits = bits
        self.coinbase_flags = coinbase_flags
        self.serializer = BlockheaderSerializer()
        self.rebuild_template()
        
    def rebuild_template(self):
        """Rebuild a version 2 blockheader and serialize it.
            
           oldest satoshi client coinbase script contains:
               nBits, bnExtraNonce (nBits = GetNextWorkRequired(pindexPrev);)
           later timestamp was used instead of "bits" to ensure coinbase txn is unique even if address is the same (github:83f4cd156e9d52bd7c4351336dfa4806a43ee4e4=.
           now in version 2 blocks the height is included instead of the timestamp.
        """
        coinbase_script = Script([push_bignum_instruction(self.block_height)] + 
                                 [push_bignum_instruction(self.extra_nonce)] +
                                 [push_data_instruction(flag) for flag in self.coinbase_flags])
        coinbase_txin = TxIn(Outpoint.null(),
                             coinbase_script,
                             sequence=TxIn.NSEQUENCE_FINAL)
        coinbase_tx = Tx(version=1,
                         in_list=[coinbase_txin],
                         out_list=self.coinbase_txout_list,
                         locktime=0)
        self.block_transactions = [coinbase_tx] + self.transactions
        self.blockheader = BlockHeader(version=2,
                                  hash_prev=self.hash_prev,
                                  hash_merkle=compute_merkle_root(self.block_transactions),
                                  time=self.time,
                                  bits=self.bits, 
                                  nonce=self.nonce)
        self.serialized = self.serializer.serialize(self.blockheader)

    def set_nonce(self, nonce):
        """Change the Nonce; Currently reserializes all. This needs to be optimized to just change the nonce bytes"""
        self.nonce = nonce
        self.rebuild_template()
        
    def set_time(self, time):
        self.time = time
        self.rebuild_template()
        
    def set_extra_nonce(self, extra_nonce):
        self.extra_nonce = extra_nonce
        self.rebuild_template()

    def get_serialized(self):
        return self.serialized

    def get_block(self):
        return Block(self.blockheader, self.block_transactions)

def default_nonce_changer(template):
    if template.nonce == BlockHeader.MAX_NONCE:
        template.set_extra_nonce(template.extra_nonce + 1)
        template.set_nonce(0)
    else:
        template.set_nonce(template.nonce + 1)

class BitcoinMiner():
    @staticmethod
    def mine_block(hash_prev,
                   block_height,
                   time_source,
                   difficulty_bits,
                   transactions, 
                   coinbase_txout_list,
                   coinbase_flags=["/P2SH/"],
                   nonce_changer=default_nonce_changer):
        template = BlockheaderTemplate(hash_prev, 
                                       block_height,
                                       coinbase_txout_list, 
                                       transactions, 
                                       time_source.get_time(), 
                                       difficulty_bits,
                                       coinbase_flags=coinbase_flags)
        difficulty_target = uint256_difficulty(difficulty_bits)
        hash_found = False
        while not hash_found:
            hash = Uint256.from_bytestr(doublesha256(template.get_serialized()))
            if (hash <= difficulty_target):
                hash_found = True
            else:
                nonce_changer(template)
        return (template.get_block(), template)

if __name__ == '__main__':
    from coinpy.model.genesis import GENESIS
    from coinpy.model.protocol.runmode import UNITNET
    from coinpy.lib.blocks.difficulty import uint256_difficulty
    from coinpy.tools.hex import decodehexstr
    from coinpy.model.scripts.instruction import Instruction
    from coinpy.model.scripts.opcodes import OP_CHECKSIG
    from coinpy.model.scripts.opcodes import OP_PUSHDATA
    from coinpy.model.scripts.script import Script
    import struct
    from coinpy.tools.hex import hexstr
    
    print hexstr(struct.pack("<I", 213566))
    print  uint256_difficulty(524287999)
    time_source = SystemTimeSource()
    miner = BitcoinMiner()
    
    block = miner.mine_block(hash_prev=Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"), 
                             block_height=0,
                             time_source=time_source, 
                             difficulty_bits=524287999, 
                             transactions=[], 
                             coinbase_txout_list=[TxOut(5000000000, Script([Instruction(OP_PUSHDATA, decodehexstr("04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")),Instruction(OP_CHECKSIG)]))],
                             coinbase_flags=[])
    print block
    