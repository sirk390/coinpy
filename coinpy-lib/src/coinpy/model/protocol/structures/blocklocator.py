
class BlockLocator():
    """List of hashes from the highest block(first dense) to the genesis block(then sparse).
    
       This can be seen as a compressed version of the complete blockchain hash list that 
       allows to find fork points with a good precision when recent and a lesser precision 
       when old.
       
       Attributes:
           version (int):
           blockhashlist (list of Uint256): list of hashes from the highest block(dens) to the genesis block(sparse)
    
    """
    def __init__(self, version, blockhashlist):
        self.version = version
        self.blockhashlist = blockhashlist
    
    def highest(self):
        return self.blockhashlist[0]
    
    def lowest(self):
        return self.blockhashlist[-1]
 
    def __eq__(self, other):
        return (self.version == other.version and 
                self.blockhashlist == other.blockhashlist)
     
    def __str__(self):
        return "BlockLocator(len=%d hashes=%s..., version=%d)" % (len(self.blockhashlist), ",".join(str(h) for h in self.blockhashlist[:5]), self.version)
