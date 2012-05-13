# -*- coding:utf-8 -*-
"""
Created on 23 Apr 2012

@author: kris
"""
from coinpy.tools.reactor.reactor import Reactor, reactor
from coinpy.tools.reactor.future import Future
import unittest
from adodbapi.adodbapi import Error
from coinpy.tools.reactor.asynch import asynch_method

# test_inline_callbacks
def slow_fct():
    print "slow_fct"
    f1 = Future()
    def done():
        print "done"
        f1.set_result(3)
    reactor.call_later(0.1, done)
    return f1

@asynch_method
def asynch_fct1():
    print "asynch_fct1"
    v1 = yield slow_fct()
    v2 = yield slow_fct()
    yield v1 * v2

@asynch_method
def asynch_fct2():
    print "asynch_fct2"
    v1 = yield asynch_fct1()
    v2 = yield asynch_fct1()
    yield v1 + v2
#  test_inline_callbacks_exception1

@asynch_method
def asynch_fct3():
    print "asynch_fct3"
    v1 = yield slow_fct()
    raise Exception("boum")
    
@asynch_method
def asynch_fct4():
    print "asynch_fct4"
    v1 = yield asynch_fct1()
    try:
        v2 = yield asynch_fct3()
    except:
        print "re-raising"
        raise
    yield v1 + v2
    

class TestFuture(unittest.TestCase):
    def test_inline_callbacks(self):
        reactor.reset()
        def print_result(result=None, error=None):
            print "result", result
            assert result == 18
        f = asynch_fct2()
        f.set_callback(print_result)
        
        reactor.call_later(0.6, reactor.stop)
        reactor.run()
        print "stop"
        assert f.completed
    
    
    def test_inline_callbacks_exception1(self):
        reactor.reset()
        def print_result(result=None, error=None):
            assert error
            print "error", error[0]
        f = asynch_fct4()
        f.set_callback(print_result)
        
        reactor.call_later(1, reactor.stop)
        reactor.run()
        print "stop"
        assert f.completed
    
if __name__ == "__main__":
    unittest.main()
