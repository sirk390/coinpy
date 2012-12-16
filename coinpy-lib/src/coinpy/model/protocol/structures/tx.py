from coinpy.model.constants.bitcoin import LOCKTIME_THRESHOLD

class Tx():
    LOCKTIME_HEIGHT, LOCKTIME_BLOCKTIME = LOCKTIME_TYPES = range(2)
    
    def __init__(self, version, in_list, out_list, locktime):
        self.version = version  
        self.in_list = in_list          
        self.out_list = out_list        
        self.locktime = locktime
        # optional extra fields used to cache the hash value once computed
        self.hash = None
        self.rawdata = None
        
    def output_count(self):
        return (len(self.out_list))
    
    def iscoinbase(self):
        return ((len(self.in_list) == 1) and 
                (self.in_list[0].previous_output.is_null()))
       
    def isstandard(self):
        if any(not script.ispushonly() for script in self.in_list):
            return (False)
        if any(not script.isstandard() for script in self.out_list):
            return (False)        
        return (True)

    def locktimetype(self):
        if (self.locktime < LOCKTIME_THRESHOLD):
            return (self.LOCKTIME_HEIGHT)
        return (self.LOCKTIME_BLOCKTIME)
        
    def isfinal(self, height, blocktime):
        if self.locktime == 0:
            return True
        if (self.locktimetype() == self.LOCKTIME_HEIGHT and self.locktime < height):
            return True
        if (self.locktimetype() == self.LOCKTIME_BLOCKTIME and self.locktime < blocktime):
            return True
        for txin in self.in_list:
            if (not txin.isfinal()):
                return False
        return True

    def __eq__(self, other):
        return (self.version == other.version and 
                self.in_list == other.in_list and 
                self.out_list == other.out_list and 
                self.locktime == other.locktime)

    def __str__(self):
        return ("tx(v:%d,in(%d)[%s...],out(%d)[%s...],lock:%d)" % 
                    (self.version, 
                     len(self.in_list), 
                     ",".join(str(o) for o in self.in_list[:5]),
                     len(self.out_list),
                     ",".join(str(o) for o in self.out_list[:5]),
                     self.locktime))
