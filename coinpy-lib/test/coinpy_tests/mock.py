# -*- coding:utf-8 -*-
"""
Created on 8 Feb 2012

@author: kris
"""

class Mock():
    """
    __init__
        specs :   {name: {args: return_value, ...}, {name: return_value, ...}, ...}
    """
    def __init__(self, specs={}, accept_all_methods=False):
        self.accept_all_methods = accept_all_methods
        self._methods = {}
        for name, spec in specs.iteritems():
            if type(spec) is not dict:
                spec = {(): spec }
            self._methods[name] = MockMethod(spec)

    def __getattr__(self, name):
        if name in self._methods:
            return self._methods[name]
        if not self.accept_all_methods:
            raise AttributeError("Mock method undefined: %s" % (name))
        self._methods[name] = MockMethod(accept_all_args=True)
        return self._methods[name]
    
    def __str__(self):
        return "{Mock}"
    
class MockMethod():
    """
    __init__
        spec: {args: return_value, ...}
               args can be a tuple, list or single item
        accept_all:
               if False, raises an exception if arguments are not defined in 
               spec, if True, returns a Mock() object.
    """
    def __init__(self, spec={}, accept_all_args=False):
        self.call_count = 0
        self.accept_all_args = accept_all_args
        self._spec = {}
        for args, return_value in spec.iteritems():
            if (type(args) is not tuple) and (type(args) is not list):
                args = (args,)
            self._spec[args] = return_value
    
    def __call__(self, *args, **kwargs):
        self.call_count += 1
        if args in self._spec:
            return self._spec[args]
        if not self.accept_all_args:
            raise Exception("Mock result_value undefined for argument")
        return Mock()
    
    called = property(lambda self: self.call_count != 0)
    
if __name__ == '__main__':
    m1 = MockMethod(spec={"a": 6, "b": 1})  
    print m1("b")
    m1 = MockMethod(accept_all_args=True)  
    print m1("c")
    
    a1 = Mock(specs={"xx": 6})              #simple return value
    a2 = Mock(specs={"xx": {"a":1, "b":2}}) #return value depends on parameter
    a3 = Mock(specs={"xx": {("a", 6) :1}})  #return value depends on multiple parameters
    a4 = Mock(accept_all_methods=True)      #accept any method
    
    a4.test("a")
    assert a4.test.called
    
    b = Mock(specs={"xx": 6, "yy":{"a": 1,("b",2) : 2}})
    print b.xx()
    assert not b.yy.called
    print b.yy("a")
    print b.yy("b", 2)
    assert b.yy.called
    