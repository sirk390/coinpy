
class Timenetaddr():
    """Timestamped netaddr"""
    def __init__(self, timestamp, netaddr):
        self.timestamp = timestamp  
        self.netaddr = netaddr
        
    def __str__(self):
        return ("%d:%s" % (self.timestamp, str(self.netaddr)))
