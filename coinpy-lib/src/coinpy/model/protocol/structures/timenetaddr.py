
class Timenetaddr():
    """Timestamped netaddr"""
    def __init__(self, timestamp, netaddr):
        self.timestamp = timestamp  
        self.netaddr = netaddr

    def __eq__(self, other):
        return (self.timestamp == other.timestamp and 
                self.netaddr == other.netaddr)
      
    def __str__(self):
        return ("%d:%s" % (self.timestamp, str(self.netaddr)))
