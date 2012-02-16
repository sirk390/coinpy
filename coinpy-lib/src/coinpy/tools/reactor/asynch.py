# -*- coding:utf-8 -*-
"""
Created on 16 Feb 2012

@author: kris
"""
import types

class Asynch():
    def __init__(self, coroutine, arg = None):
        self.coroutine = [coroutine()]
        self.args = [arg]
        self.iscompleted = False
        self.return_value = None
        
    def run(self):
        try:
            result = self.coroutine[-1].send(self.args[-1])
            if type(result) is types.GeneratorType:
                self.coroutine.append(result)
                self.args.append(None)
            else:
                self.args[-1] = result  
                
        except StopIteration as e:
            if (len(self.coroutine) == 1):
                self.iscompleted = True
                self.return_value = self.args[-1]
            else:
                self.coroutine.pop()
                result = self.args.pop()
                self.args[-1] = result
                            
    def completed(self):
        return self.iscompleted


if __name__ == '__main__':
    #Example usage
    def slow_func_0_1(x):
        return x + 1
    def slow_func_0_2(x):
        return x + 1
    def slow_func1(x):
        x = yield slow_func_0_1(x)
        x = yield slow_func_0_2(x)
        yield x
    def slow_func2(x):
        yield x * 2
    def asynch_func1():
        a = yield slow_func1(1)
        b = yield slow_func2(a)
        yield b
    
    a = Asynch(asynch_func1)
    while not a.completed():
        a.run()
    print a.return_value
    
