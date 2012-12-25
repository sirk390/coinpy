
class Netaddr():
    """Bitcoin node network address.
    
    Attributes:
       services (SERVICES_NONE=0 or SERVICES_NODE_NETWORK=1)
       ip (string)
       port (int)
    """
    def __init__(self, services, ip, port):
        self.services = services
        self.ip = ip
        self.port = port
    
    def __eq__(self, other):
        return (self.services == other.services and 
                self.ip == other.ip and 
                self.port == other.port)

    def __str__(self):
        return ("%s:%d(%d)" % (self.ip, self.port, self.services))
