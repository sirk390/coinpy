# -*- coding:utf-8 -*-
"""
Created on 16 Feb 2012

@author: kris
"""
import traceback
from coinpy.tools.reactor.future import Future
from coinpy.tools.reactor.reactor import reactor

"""
Note: in case of error, the error contains "(exception, traceback_string)"
"""
def process_coroutines(gen, future, result=None, error=None):
    try:
        if error:
            exc, tbstr = error
            result = gen.throw(exc)
        else:
            result = gen.send(result)
    except StopIteration as e:
        future.set_result(result)
        return
    except Exception as e:
        print traceback.format_exc()
        future.set_error( (e, traceback.format_exc()) )
        return
    if type(result) is Future:
        result.set_callback(process_coroutines, (gen, future))
    else:
        reactor.call(process_coroutines, gen, future, result=result)

def asynch_method(method):
    """  Decorator inspired by twistedMatrix.inlineCallbacks.
    
     Can be used for both CPU bound methods and IO bound methods.
         - yield a 'Future'. The method will continue at
         the same point when the 'Future' completes.
         - yield nothing, and the method will continue when the reactor has time. 
         This enables to share CPU time.
         
     - should we add a reactor argument to this decorator?
     - or add an keyword-only argument to the method (python > 3.0)
    """
    def new_method(*args):
        future = Future()
        gen = method(*args)
        reactor.call(process_coroutines, gen, future)
        return future
    return new_method