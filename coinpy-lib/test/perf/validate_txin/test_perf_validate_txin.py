# -***- coding:utf-8 -*-
"""
Created on 12 May 2012

@author: kris
"""

import unittest
import cPickle
from coinpy.lib.vm.vm import TxValidationVM
import time
import traceback
import multiprocessing
import random

vm = TxValidationVM()

def validate_txin(input):
    tx, index, txout = input
    if not vm.validate(tx, index, txout.script, tx.in_list[index].script):
        return False
    return True

def validate_txin_mock(input):
    tx, index, txout = input
    return True
               
class TestPerfValidateTxin(unittest.TestCase):
    def setUp(self):
        with open("1000_txin_1.pkl", "rb") as f:
            self.txin_1000_2 = cPickle.load(f)

        self.txin_100 = random.sample(self.txin_1000_2, 100)
    
    def test_validate_1000_txin(self):
        t1 = time.time()
        for tx, index, prev_txout in self.txin_1000_2:
            assert vm.validate(tx, index, prev_txout.script, tx.in_list[index].script)
        t2 = time.time()
        print "Validated 1000 txin: %f ms/txin" % (t2 - t1)
        

    def test_validate_1000_txin_parallel(self):
        nb_processes = 4
        process_pool = multiprocessing.Pool(nb_processes)
        t1 = time.time()
        f = process_pool.map_async(validate_txin, self.txin_1000_2, 1)
        result = f.get()
        assert all(result)
        t2 = time.time()
        print "Validated 1000 txin: %f ms/txin (%d processes)" % (t2 - t1, nb_processes)


    def test_validate_100_txin_parallel(self):
        nb_processes = 4
        process_pool = multiprocessing.Pool(nb_processes)
        t1 = time.time()
        f = process_pool.map_async(validate_txin, self.txin_100, 1)
        result = f.get()
        assert all(result)
        t2 = time.time()
        print "Validated %f ms/txin (100 txin, %d processes)" % ((t2 - t1) * 10, nb_processes)


    def test_validate_1000_txin_overhead(self):
        nb_processes = 4
        process_pool = multiprocessing.Pool(nb_processes)
        t1 = time.time()
        f = process_pool.map_async(validate_txin_mock, self.txin_1000_2, 1)
        result = f.get()
        assert all(result)
        t2 = time.time()
        print "parallelisation overhead cost: %f ms/txin (1000 txin, %d processes)" % (t2 - t1, nb_processes)

    def test_validate_100_txin_overhead(self):
        nb_processes = 4
        process_pool = multiprocessing.Pool(nb_processes)
        t1 = time.time()
        f = process_pool.map_async(validate_txin_mock, self.txin_100, 1)
        result = f.get()
        assert all(result)
        t2 = time.time()
        print "parallelisation overhead cost: %f ms/txin (100 txin, %d processes)" % ((t2 - t1) * 10, nb_processes)


if __name__ == '__main__':
    unittest.main()
    