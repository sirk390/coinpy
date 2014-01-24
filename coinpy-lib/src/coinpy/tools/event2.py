from coinpy.tools.reactor.reactor import reactor

class AllreadySubscribedException(Exception):
    pass
class NotSubscribedException(Exception):
    pass
class DuplicateKeywordArgument(Exception):
    pass

class CallArgs(object):
    """ Optional arguments + keyword arguments given to a function
        They can be added together as below:
        >> CallArgs(args=("a", "b"), kwargs={"c":"d"}) + CallArgs(args=("e", "f"), kwargs={"g":"h"})
        <CallArgs:a,b,e,f,c:d,g:h>
    """
    def __init__(self, args=None, kwargs=None):
        self.args = args or ()
        self.kwargs = kwargs or {}
        
    def __eq__(self, other):
        return (self.args == other.args and 
                self.kwargs == other.kwargs)
        
    def __add__(self, other):
        for k in other.kwargs:
            if k in self.kwargs:
                raise DuplicateKeywordArgument("Duplicate keyword argument: %s" % (k))
        kwargs = dict(self.kwargs)
        kwargs.update(other.kwargs)
        return CallArgs(self.args + other.args, kwargs)
    
class Listener(object):
    """ Callback and arguments to be called on completion of an Event """
    def __init__(self, fct, callargs=None):
        self.fct = fct
        self.callargs = callargs or CallArgs()
        
    def __eq__(self, other):
        return (self.fct == other.fct and 
                self.callargs == other.callargs)

def synchcall(f, *args, **kwargs):
    """ Synchronous function call """
    return f(*args, **kwargs)

class Event(object):
    """Implementation of the observer pattern.
       
       Both "subscribe" and "fire" support optional and keyword argument.
       When fired, the callback will be called with both the arguments of the subscribe and the arguments of the fire.
       
       A special "call_method" argument allows to run the Even callbacks on an 
       Event Loop e.g:
           CHANGED = Event(event_loop.callLater)
        
    Example
    -------
      class A()
          def __init__(self): 
              self.CHANGED = Event()
          def a():
              self.CHANGED.fire()
      a = A()
      def handler(e, some_value):
          print "hello", some_value
      a.CHANGED.subscribe(handler, some_value="world")
      a.a()
    
    """
    def __init__(self, call_method=synchcall, listeners=None):
        self.listeners = listeners or {}
        self.call_method = call_method
    
    def get_listeners(self):
        return self.listeners.values()

    def get_listener(self, fct):
        return self.listeners[fct]
    
    def get_listeners_methods(self):
        return self.listeners.keys()
    
    def is_subscribed(self, callback):
        return callback in self.listeners
    
    def subscribe(self, callback, *args, **kwargs):
        if callback in self.listeners:
            raise AllreadySubscribedException(callback)
        self.listeners[callback] = Listener(callback, CallArgs(args, kwargs))
        
    def unsubscribe(self, callback):
        if callback not in self.listeners:
            raise NotSubscribedException(callback)
        del self.listeners[callback]
        
    def fire(self, *args, **kwargs):
        for listener in self.listeners.values():
            args = listener.callargs + CallArgs(args, kwargs)
            self.call_method(listener.fct, *args.args, **args.kwargs)
    
    @classmethod
    def with_listerners(cls, listerners):
        return cls(listeners=dict((l.fct, l) for l in listerners))
    

    