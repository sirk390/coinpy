import unittest

from coinpy.model.protocol.structures.block import Block
from coinpy.model.protocol.structures.blockheader import BlockHeader
from coinpy.lib.blockchain.bockchain_work import DifficultyIterator, get_work_required, retarget, adjust
from coinpy.model.protocol.runmode import TESTNET, TESTNET3, MAIN
from coinpy.lib.blocks.difficulty import uint256_difficulty, compact_difficulty
from coinpy.model.constants.bitcoin import TARGET_TIMESPAN, PROOF_OF_WORK_LIMIT

class StaticDifficultyHistory(DifficultyIterator):
    def __init__(self, history):
        #list of (height, time, difficulty(compact format) )
        self.history = history
        
    def get_item(self, height):
        if height in self.history:
            return self.history[height]
        raise Exception("Not found: %d" % (height))
    

class TestBlockchainWork(unittest.TestCase):
    def setUp(self):
        pass

    def test_blockchain_retarget(self):
        # Standard case retarget (taken from block 46368)
        self.assertEquals(retarget(1268010873, 1269211443, 
                                   TARGET_TIMESPAN, 
                                   473464687, 
                                   PROOF_OF_WORK_LIMIT[MAIN]),
                          473437045)
        # Limit adjustment step as in block 68544 "actual_timespan < TARGET_TIMESPAN/4"
        self.assertEquals(retarget(1279008237, 1279297671, 
                                   TARGET_TIMESPAN, 
                                   470131700, 
                                   PROOF_OF_WORK_LIMIT[MAIN]),
                          469854461)
        # Limit adjustment step "actual_timespan > TARGET_TIMESPAN/4"
        self.assertEquals(retarget(1357060298, 1363713098, 
                                   TARGET_TIMESPAN, 
                                   470131700, 
                                   PROOF_OF_WORK_LIMIT[MAIN]),
                          471240656)
        # Min to the proof of work  limit
        self.assertEquals(retarget(1357060298, int(1357060298+TARGET_TIMESPAN*1.5), 
                                   TARGET_TIMESPAN, 
                                   compact_difficulty(PROOF_OF_WORK_LIMIT[MAIN]), 
                                   PROOF_OF_WORK_LIMIT[MAIN]),
                          compact_difficulty(PROOF_OF_WORK_LIMIT[MAIN]))

    def test_blockchain_adjust(self):
        # normal case, last not specific difficulty (2016 here)
        difficulty_history1 = StaticDifficultyHistory({
            2015 : DifficultyIterator.Difficulty(time=1357060298, bits=473464683),
            2016 : DifficultyIterator.Difficulty(time=1357060898, bits=473464684),
            2017 : DifficultyIterator.Difficulty(time=1357061498, bits=compact_difficulty(PROOF_OF_WORK_LIMIT[TESTNET])),
            2018 : DifficultyIterator.Difficulty(time=1357062098, bits=compact_difficulty(PROOF_OF_WORK_LIMIT[TESTNET]))})
        self.assertEquals(adjust(2019, difficulty_history1, 1357062698, PROOF_OF_WORK_LIMIT[TESTNET]),
                          473464684)  
        # no block mined since 2*TARGET_SPACING => reset to PROOF_OF_WORK_LIMIT
        difficulty_history2 = StaticDifficultyHistory({
            3500 : DifficultyIterator.Difficulty(time=1357060298, bits=373464683)})
        self.assertEquals(adjust(3501, difficulty_history2, 1357061499, PROOF_OF_WORK_LIMIT[TESTNET]),
                          compact_difficulty(PROOF_OF_WORK_LIMIT[TESTNET]))
        
    def test_blockchain_get_work_required_main(self):
        # Simply copy previous difficulty if height % TARGET_INTERVAL != 0
        main_difficulty_history_46367 = StaticDifficultyHistory({
            46366 : DifficultyIterator.Difficulty(time=1269210928, bits=473464687)})
        self.assertEquals(get_work_required(46367,
                                            main_difficulty_history_46367,
                                            1269212064, MAIN), 473464687)
         
        # Retarget  if height % TARGET_INTERVAL == 0
        # (block 46368 depends on block times of 44352, 46367 and target of block 46367)
        main_difficulty_history_46368 = StaticDifficultyHistory({
            44352 : DifficultyIterator.Difficulty(time=1268010873, bits=473464687) ,
            46367 : DifficultyIterator.Difficulty(time=1269211443, bits=473464687)})
        self.assertEquals(get_work_required(46368,
                                            main_difficulty_history_46368,
                                            1269212064, MAIN), 473437045)
        
    def test_blockchain_get_work_required_testnet(self):
        # testnet adjusting algorithm (Min to the proof of work  limit)
        difficulty_history = StaticDifficultyHistory({
            3500 : DifficultyIterator.Difficulty(time=1357060298, bits=373464683)})
        self.assertEquals(get_work_required(3501, difficulty_history, 1357061499, TESTNET),
                          compact_difficulty(PROOF_OF_WORK_LIMIT[TESTNET]))

    def get_outpoint(self, outpoint):
        pass
    
if __name__ == '__main__':
    unittest.main()
