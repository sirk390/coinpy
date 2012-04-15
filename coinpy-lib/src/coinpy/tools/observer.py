class Event(object):
    def __str__(self):
        return (str(self.__dict__))
    
class Observable(object):
    lastevent = 0
    
    def __init__(self, reactor):
        self.reactor = reactor
        self.listeners = {}
        
    @classmethod 
    def createevent(cls):
        cls.lastevent += 1
        return (cls.lastevent)
        
    def subscribe(self, eventtype, callback):
        if (eventtype not in self.listeners):
            self.listeners[eventtype] = set()
        self.listeners[eventtype].add(callback)
        
    def unsubscribe(self, eventtype, callback):
        self.listeners[eventtype].remove(callback)
        
    def fire(self, eventtype, **attrs):
        if (eventtype in self.listeners):
            e = Event()
            e.source = self
            for k, v in attrs.iteritems():
                setattr(e, k, v)
            for fn in self.listeners[eventtype]:
                if self.reactor: #speed up by remove test?
                    self.reactor.call(fn, e)
                else:
                    fn(e)
           
        