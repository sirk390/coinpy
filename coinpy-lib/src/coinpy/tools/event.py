from coinpy.tools.reactor.reactor import reactor

class Notification(object):
    pass
    
class Event(object):
    """ Simpler implementation of the observer pattern (unrelated to  observer.py)
    
    Example
    -------
      class A()
          def __init__(self): 
              self.CHANGED = Event()
          def a():
              self.CHANGED.fire()
      a = A()
      def handler(e):
          print "changed"
      a.CHANGED.subscribe(handler)
      a.a()
    
    """
    def __init__(self):
        self.listeners = set()
        
    def subscribe(self, callback):
        self.listeners.add(callback)
        
    def unsubscribe(self, callback):
        self.listeners.remove(callback)
        
    def fire(self, **attrs):
        n = Notification()
        for k, v in attrs.iteritems():
            setattr(n, k, v)
        for listener in  self.listeners:
            listener(n)
