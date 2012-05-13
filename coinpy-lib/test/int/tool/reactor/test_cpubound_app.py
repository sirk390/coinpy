# -*- coding:utf-8 -*-
"""
Created on 23 Apr 2012

@author: kris
"""
from coinpy.tools.reactor.reactor import Reactor, reactor
from coinpy.tools.reactor.future import Future
import unittest
from coinpy.tools.reactor.asynch import asynch_method

def slow_fct():
    return sum(i for i in range(1000000))

@asynch_method
def asynch_fct1(n):
    print "asynch_fct1"
    v1 = 0 
    for i in range(5):
        v1 += yield slow_fct()
        print n
    yield v1    

    
class TestCPUBound(unittest.TestCase):
    """ CPU time is shared between 'a' and 'b' instances of asynch_fct1"""
    def test_cpu_bound(self):
        def print_result(result=None, error=None):
            print "result", result
            assert result == 2499997500000
        f1 = asynch_fct1("a")
        f2 = asynch_fct1("b")
        f1.set_callback(print_result)
        f2.set_callback(print_result)
        print "start"
        reactor.call_later(3, reactor.stop)
        reactor.run()
        print "stop"
    
if __name__ == "__main__":
    unittest.main()

