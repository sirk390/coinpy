
class WalletPoolKey(object):
    def __init__(self, poolnum, version, time, public_key):
        self.poolnum, self.version, self.time, self.public_key = poolnum, version, time, public_key
    
    def __str__(self):
        return "WalletPoolKey(num:%d, time:%d public_key:%s)" % (self.poolnum, self.time, str(self.public_key))
