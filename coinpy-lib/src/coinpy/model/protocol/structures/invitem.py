INV_TX = 1
INV_BLOCK = 2
INV_ITEMS = (INV_TX, INV_BLOCK)

class Invitem():
    def __init__(self, type, hash):
        self.type = type
        self.hash = hash 

    def __eq__(self, other):
        return (self.type == other.type and 
                self.hash == other.hash)
     
    def __str__(self):
        legend = {INV_TX:"TX", INV_BLOCK:"BLK"}
        return ("%s:%s" % (legend.get(self.type, "ERR"), str(self.hash)))
        
    