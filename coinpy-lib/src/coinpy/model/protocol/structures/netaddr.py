
class Netaddr():
    def __init__(self, services, ip, port):
        self.services = services    #int (bitfield)
        self.ip = ip                #string "a.b.c.d"
        self.port = port            #int
    
    def __eq__(self, other):
        return (self.services == other.services and 
                self.ip == other.ip and 
                self.port == other.port)

    def __str__(self):
        return ("%s:%d(%d)" % (self.ip, self.port, self.services))
