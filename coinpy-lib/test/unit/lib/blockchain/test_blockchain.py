import unittest
from coinpy_tests.mock import Mock, MockMethod
from coinpy.lib.bitcoin.blockchain.blockchain import Blockchain
from coinpy.model.protocol.structures.block import Block
from coinpy.model.protocol.structures.blockheader import BlockHeader

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_blockchain_append_mainchain(self):
        parent_block_hash = "prevblock_hash"
        blockhash = "somehash"
        block = Block(BlockHeader(version=1, 
                                  hash_prev=parent_block_hash, 
                                  hash_merkle="hash_merkle", 
                                  time=323, 
                                  bits=243, 
                                  nonce=12), [])
        log = Mock(accept_all_methods=True)
        block_handle = Mock({"get_block" : block})
        parent_block_handle = Mock({"is_mainchain" : True})
        database = Mock({"append_block" : {(blockhash, block) : block_handle},
                         "get_block_handle" : {parent_block_hash : parent_block_handle}}, 
                         accept_all_methods=True)
        bc = Blockchain(log, database)
        bc.appendblock("somehash", block)
        
        assert database.begin_updates.called
        assert database.append_block.called
        assert database.commit_updates.called
        assert not database.set_mainchain.called
        
    def test_blockchain_append_altchain_lesswork(self):
        parent_block_hash = "prevblock_hash"
        blockhash = "somehash"
        besthash = "besthash"
        blockheader = Mock({"work": 1}, attributes={"hash_prev": parent_block_hash})
        block = Mock(attributes={"blockheader":blockheader, "transactions" : []})
        log = Mock(accept_all_methods=True)
        block_handle = Mock({"get_block" : block})
        parent_block_handle = Mock({"is_mainchain" : False}, attributes={"hash": parent_block_hash})
        database = Mock({"append_block" : {(blockhash, block) : block_handle},
                         "get_block_handle" : {parent_block_hash : parent_block_handle},
                         "get_mainchain" : besthash}, 
                         accept_all_methods=True)
        fork_block_hash = "fork_hash"
        fork_block_handle =  Mock(attributes={"hash": fork_block_hash})
        mainbranch =  Mock({"work": 5})
        altbranch = Mock({"work": 3})
         
        bc = Blockchain(log, database)
        bc.get_branch = MockMethod({(fork_block_hash, parent_block_hash) : altbranch,
                                    (fork_block_hash, besthash): mainbranch})
        bc.get_mainchain_parent = MockMethod({parent_block_handle : fork_block_handle})

        bc.appendblock("somehash", block)
        
        assert database.begin_updates.called
        assert database.append_block.called
        assert database.commit_updates.called
        assert not database.set_mainchain.called
        
    def test_blockchain_append_altchain_morework(self):
        parent_block_hash = "prevblock_hash"
        blockhash = "somehash"
        besthash = "besthash"
        blockheader = Mock({"work": 2}, attributes={"hash_prev": parent_block_hash})
        block = Mock(attributes={"blockheader":blockheader, "transactions" : []})
        log = Mock(accept_all_methods=True)
        block_handle = Mock({"get_block" : block})
        parent_block_handle = Mock({"is_mainchain" : False}, attributes={"hash": parent_block_hash})
        database = Mock({"append_block" : {(blockhash, block) : block_handle},
                         "get_block_handle" : {parent_block_hash : parent_block_handle},
                         "get_mainchain" : besthash}, 
                         accept_all_methods=True)
        fork_block_hash = "fork_hash"
        fork_block_handle =  Mock(attributes={"hash": fork_block_hash})
        mainbranch =  Mock({"work": 5, "__iter__" : iter([])})
        altbranch = Mock({"work": 4, "__iter__" :  iter([])})
         
        bc = Blockchain(log, database)
        bc.get_branch = MockMethod({(fork_block_hash, parent_block_hash) : altbranch,
                                    (fork_block_hash, besthash): mainbranch})
        bc.get_mainchain_parent = MockMethod({parent_block_handle : fork_block_handle})

        bc.appendblock("somehash", block)
        
        assert database.begin_updates.called
        assert database.append_block.called
        assert database.commit_updates.called
        assert database.set_mainchain.called # with parent_block_hash

if __name__ == '__main__':
    unittest.main()
    
