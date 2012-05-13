# -*- coding:utf-8 -*-
"""
Created on 12 May 2012

@author: kris
"""

import unittest
import cPickle
from coinpy.lib.vm.vm import TxValidationVM
import time

class TestPerfValidateTxin(unittest.TestCase):
    def setUp(self):
        with open("1000_txin_1.pkl", "rb") as f:
            self.txin_1000_2 = cPickle.load(f)
        self.vm = TxValidationVM()
    
    def test_validate_1000_txin(self):
        t1 = time.time()
        for tx, index, prev_txout in self.txin_1000_2:
            assert self.vm.validate(tx, index, prev_txout.script, tx.in_list[index].script)
        t2 = time.time()
        print "Validated 1000 txin: %f ms/txin" % (t2 - t1)
        
if __name__ == '__main__':
    unittest.main()
    