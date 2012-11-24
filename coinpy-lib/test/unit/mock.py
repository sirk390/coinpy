
class Mock():
    """
    __init__
        specs :   {name: {args: return_value, ...}, {name: return_value, ...}, ...}
    """
    def __init__(self, methods={}, attributes={}, accept_all_methods=False):
        self.accept_all_methods = accept_all_methods
        self._methods = dict((name, MockMethod(methods)) for name, methods in methods.iteritems())
        self._attributes = attributes

    def __getattr__(self, name):
        if name in self._methods:
            return self._methods[name]
        if name in self._attributes:
            return self._attributes[name]
        if not self.accept_all_methods:
            raise AttributeError("Mock method undefined: %s" % (name))
        self._methods[name] = MockMethod(accept_all_args=True)
        return self._methods[name]
    
    def __str__(self):
        return "{Mock}"

    def __hash__(self):
        return id(self)
    
class MockMethod():
    """
    __init__
        spec: {args: return_value, ...}
               args can be a tuple, list or single item
        accept_all:
               if False, raises an exception if arguments are not defined in 
               spec, if True, returns a Mock() object.
    """
    def __init__(self, method={}, accept_all_args=False):
        self.call_count = 0
        self.accept_all_args = accept_all_args
        #allow for simple return_value arguments
        if type(method) is not dict:
            method = {(): method }
        self._spec = {}
        for args, return_value in method.iteritems():
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
    
    def __hash__(self):
        return id(self)
    
    called = property(lambda self: self.call_count != 0)
    
if __name__ == '__main__':
    m1 = MockMethod(method={"a": 6, "b": 1})  
    print m1("b")
    m1 = MockMethod(accept_all_args=True)  
    print m1("c")
    
    a1 = Mock(methods={"xx": 6})              #simple return value
    a2 = Mock(methods={"xx": {"a":1, "b":2}}) #return value depends on parameter
    a3 = Mock(methods={"xx": {("a", 6) :1}})  #return value depends on multiple parameters
    a4 = Mock(accept_all_methods=True)      #accept any method
    a5 = Mock(methods={"xx": {"x" :1}}, accept_all_methods=True)      #return value depends on parameters + accept any method
    a6 = Mock(methods={"xx": {"x" :1}}, attributes={'c' : 5})      #return value depends on parameters + attribute
   
    a4.test("a")
    assert a4.test.called
    
    b = Mock(methods={"xx": 6, "yy":{"a": 1,("b",2) : 2}})
    print b.xx()
    assert not b.yy.called
    print b.yy("a")
    print b.yy("b", 2)
    assert b.yy.called
    