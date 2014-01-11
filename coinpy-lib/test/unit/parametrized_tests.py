""" https://bitbucket.org/lothiraldan/unittest-templates/ WTFPL"""
from functools import (partial, wraps)
import re

def testcases(args):
    def wrapper(func):
        func.testcases = args
        return func
    return wrapper

def method_partial(func, *parameters, **kparms):
    @wraps(func)
    def wrapped(self, *args, **kw):
        kw.update(kparms)
        return func(self, *(args + parameters), **kw)
    return wrapped

def stringify_arguments(args):
    return "__".join([re.sub("[^\w]+", "_", str(a)) for a in args])

def find_unused_name(name, usednames):
    result, n = name, 0
    while result in usednames:
        n += 1
        result = "%s_test%d" % (name , n)
    return result

class UseParametrizedTests(type):
    def __new__(cls, name, bases, attr):
        for name, method in attr.items():
            if hasattr(method, "testcases"):
                for args in method.testcases:
                    new_name = "%s__%s" % (name, stringify_arguments(args))
                    unused_new_name = find_unused_name(new_name, attr)
                    attr[new_name] = method_partial(method, *args)
                    attr[new_name].__name__ = new_name
                del attr[name]
                
        return type(name, bases, attr)

def Call(*args, **kwargs):
    return (args, kwargs)
