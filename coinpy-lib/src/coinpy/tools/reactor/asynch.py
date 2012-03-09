# -*- coding:utf-8 -*-
"""
Created on 16 Feb 2012

@author: kris
"""
import types
import traceback

class Asynch(object):
    def __init__(self, coroutine, callback=None, callback_args=[]):
        self.coroutine = coroutine
        self.stack = [self.coroutine]
        self.value = None
        self.completed = False
        self.return_value = None
        self.callback = callback
        self.callback_args = callback_args
        
    def run(self):
        try:
            if type(self.value) is Exception:
                result = self.stack[-1].throw(self.value)
            else:
                result = self.stack[-1].send(self.value)
        except StopIteration as e:
            if (len(self.stack) == 1):
                self.completed = True
                self.return_value = self.value
                if self.callback:
                    self.callback(result=self.return_value, *self.callback_args)
            else:
                self.stack.pop()
            return
        except Exception as e:
            if (len(self.stack) == 1):
                self.completed = True
                self.return_value = e
                if self.callback:
                    self.callback(error=traceback.format_exc(), *self.callback_args)
            else:
                self.stack.pop()
            result = e
        if type(result) is Asynch:
            self.stack.append(result.coroutine)
            self.value = None
        else:
            self.value = result  
            
    def run_synchronously(self):
        while not self.completed:
            self.run()
        return self.return_value
    
def asynch_method(method):
    """Decorator for async methods"""
    def new_method(*args):
        return Asynch(method(*args))
    return new_method

if __name__ == '__main__':
    #Example 
    def slow_func_0_1(x):
        print "slow_func_0_1"
        return x + 1
    def slow_func_0_2(x):
        print "slow_func_0_2"
        return x + 1
    
    @asynch_method
    def slow_func1(x):
        print "slow_func1"
        x = yield slow_func_0_1(x)
        x = yield slow_func_0_2(x)
        yield x

    @asynch_method
    def slow_func2(x):
        print "slow_func2"
        raise Exception("test")
    
    @asynch_method
    def asynch_func1(a):
        print "asynch_func1"
        b = yield slow_func1(a)
        b = 9
        try:
            c = yield slow_func2(b)
        except:
            print "error"
            c = 9
        yield c
        
    def print_result_callback(result=None, error=None):
        if error:
            raise error
        print "result", result

    a = asynch_func1(1)
    a.callback = print_result_callback
    while not a.completed:
        a.run()
    print a.return_value
    
