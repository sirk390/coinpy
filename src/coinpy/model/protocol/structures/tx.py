# -*- coding:utf-8 -*-
"""
Created on 22 Jun 2011

@author: kris
"""
from coinpy.model.constants.bitcoin import is_money_range, LOCKTIME_THRESHOLD

class tx():
    LOCKTIME_HEIGHT, LOCKTIME_BLOCKTIME = LOCKTIME_TYPES = range(2)
    
    def __init__(self, version, in_list, out_list, locktime):
        self.version = version  
        self.in_list = in_list          
        self.out_list = out_list        
        self.locktime = locktime
        self.basic_check()
        
    #todo in serialisation:   size < MAX_BLOCK_SIZE
    #                         coinbase  => scriptsize
    #                         !coinbase => prevout!=null
    def basic_check(self):
        assert self.in_list and self.out_list
        for txout in self.out_list:
            assert is_money_range(txout.value)
        assert is_money_range(sum(txout.value for txout in self.out_list))
        
    def iscoinbase(self):
        return ((len(self.in_list) == 1) and 
                (self.in_list[0].previous_output.is_null()))
    
    def iterscripts(self):
        for txin in self.in_list:
            yield (txin.script)
        for txout in self.out_list:
            yield (txout.script)
        
    def max_script_sig_op_count(self):
        return (max(script.sig_op_count() for script in self.iterscripts()))

    def max_script_multisig_op_count(self):
        return (max(script.multisig_op_count() for script in self.iterscripts()))
    
    def isstandard(self):
        if any(not script.ispushonly() for script in self.in_list):
            return (False)
        if any(not script.isstandard() for script in self.out_list):
            return (False)        
        return (True)

    def locktimetype(self):
        if (self.locktime < LOCKTIME_THRESHOLD):
            return (self.LOCKTIME_HEIGHT)
        return (self.LOCKTIME_BLOCKTIME)
        
    def isfinal(self, height, blocktime):
        if self.locktime == 0:
            return True
        if (self.locktimetype() == self.LOCKTIME_HEIGHT and self.locktime < height):
            return True
        if (self.locktimetype() == self.LOCKTIME_BLOCKTIME and self.locktime < blocktime):
            return True
        for txin in self.in_list:
            if (not txin.isfinal()):
                return False
        return True
          
    def __str__(self):
        return ("tx(v:%d,in(%d)[%s...],out(%d)[%s...],lock:%d)" % 
                    (self.version, 
                     len(self.in_list), 
                     ",".join(str(o) for o in self.in_list[:5]),
                     len(self.out_list),
                     ",".join(str(o) for o in self.out_list[:5]),
                     self.locktime))
