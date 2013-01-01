from coinpy.model.constants.bitcoin import TARGET_SPACING, PROOF_OF_WORK_LIMIT,\
    TARGET_INTERVAL, TARGET_TIMESPAN
from coinpy.lib.blocks.difficulty import compact_difficulty, uint256_difficulty
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.tools.functools import first, nth
import itertools
import collections
from coinpy.model.protocol.runmode import TESTNET, TESTNET3, MAIN

#See GetNextWorkRequired: main.cpp:819

class DifficultyHistory(object):
    """ time(int) + target(Uint256) organized by heigth.
    
    This allows to test blockchain difficulty algorithms without
    requiring full blockheaders.
    """
    Item = collections.namedtuple("DifficultyHistory", "time bits")
    def get_item(self, n):
        pass
    
def retarget(time_2weekago, 
             time_now, 
             target_timespan,
             current_target, # compact format
             proof_of_work_limit):
    actual_timespan = time_now - time_2weekago
    # Limit adjustment step
    if actual_timespan < target_timespan/4:
        actual_timespan = target_timespan/4;
    if actual_timespan > target_timespan*4:
        actual_timespan = target_timespan*4;
    # Retarget
    new_target = Uint256.from_bignum(uint256_difficulty(current_target).get_bignum() * actual_timespan / target_timespan)
    if new_target > proof_of_work_limit:
        new_target = proof_of_work_limit
    return compact_difficulty(new_target)

def adjust(height, difficulty_history, current_time, proof_of_work_limit):
    """ Testnet>1329264000 and Testnet3 difficulty adjusting algorithm.
    
        If there is not block during 2*TARGET_SPACING, reset difficulty to min-difficulty
    """
    prevblocktime = difficulty_history.get_item(height-1).time
    if (current_time - prevblocktime > TARGET_SPACING * 2 or 
        current_time < prevblocktime):
        #reset difficulty to min-difficulty
        return compact_difficulty(proof_of_work_limit)
    else:
        #keep the last non-special difficulty
        h = height - 1
        d = difficulty_history.get_item(h).bits
        while (h % TARGET_INTERVAL != 0 and d == compact_difficulty(proof_of_work_limit)):
            h -= 1
            d = difficulty_history.get_item(h).bits
        return d

def get_retargeted_difficulty(height, difficulty_history, runmode):
    # Note the "off-by-one" bug (2015 instead of 2016) 
    # E.g. 2015 differences in block times, but using a TARGET_TIMESPAN of 2016
    return retarget(difficulty_history.get_item(height-TARGET_INTERVAL).time, 
                    difficulty_history.get_item(height-1).time, 
                    TARGET_TIMESPAN,
                    difficulty_history.get_item(height-1).bits,
                    PROOF_OF_WORK_LIMIT[runmode])

def normal_difficulty(height, 
                      difficulty_history,
                      runmode):
    if height % TARGET_INTERVAL!= 0:
        return difficulty_history.get_item(height-1).bits
    return get_retargeted_difficulty(height, difficulty_history, runmode)

def adjusting_difficulty(height, 
                         difficulty_history,
                         current_blocktime,
                         runmode):
    if height % TARGET_INTERVAL != 0:
        return adjust(height, difficulty_history, current_blocktime, PROOF_OF_WORK_LIMIT[runmode])
    return get_retargeted_difficulty(height, difficulty_history, runmode)

def get_work_required(height,
                      difficulty_history,
                      current_blocktime,
                      runmode):
    if (runmode == TESTNET and current_blocktime > 1329264000 or
        runmode == TESTNET3):
        return adjusting_difficulty(height, difficulty_history, current_blocktime, runmode)
    return normal_difficulty(height, difficulty_history, runmode)


