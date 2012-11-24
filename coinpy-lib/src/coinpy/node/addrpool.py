from coinpy.tools.observer import Observable
import random

class AddrPool(Observable):
    EVT_ADDED_ADDR = Observable.createevent()
    EVT_ADDED_BANNED = Observable.createevent()
    def __init__(self):
        super(AddrPool, self).__init__()
        self.known_peers = set()
        self.banned_peers = set()
    
    def addpeer(self, sockaddr):
        if sockaddr not in self.known_peers and \
            sockaddr not in self.banned_peers :
            self.known_peers.add(sockaddr)
            self.fire(self.EVT_ADDED_ADDR, addr=sockaddr)
        
    def log_failure(self, time, sockaddr):
        if sockaddr in self.known_peers:
            self.known_peers.remove(sockaddr)
    
    def log_success(self, time, sockaddr):
        pass
    
    
    def misbehaving(self, sockaddr, reason):
        if sockaddr in self.known_peers:
            self.known_peers.remove(sockaddr)
        if sockaddr not in self.banned_peers:
            self.fire(self.EVT_ADDED_BANNED, sockaddr=sockaddr, reason=reason)
            self.banned_peers.add(sockaddr)
    
    '''Get peers from the addr pool.
        
        Exclude peers for "exlude" list (e.g. usually allready connected/connecting peers)
    '''
    def getpeers(self, count, exclude=[]):
        peers = set(random.sample(self.known_peers, min(count+len(exclude), len(self.known_peers))))
        peers -= set(exclude)
        return random.sample(peers, min(len(peers), count))
    