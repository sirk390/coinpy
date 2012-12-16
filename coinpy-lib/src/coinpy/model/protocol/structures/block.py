
class Block():
    """A Block defined in the bitcoin protocol.
    
       Attributes:
           blockheader (Blockheader): block header information. 
           transactions (list of Tx): list of transactions.
    """
    def __init__(self,
                 blockheader,
                 transactions):
        self.blockheader = blockheader
        self.transactions = transactions
        # Cached value of the serialized block data.
        self.rawdata = None 
        
    def __eq__(self, other):
        return (self.blockheader == other.blockheader and 
                self.transactions == other.transactions)
  
    def __str__(self):
        return ("Block(%s, transactions(%d)[%s...])" % 
                    (str(self.blockheader), 
                     len(self.transactions),
                     ",".join([str(t) for t in self.transactions[:5]])))
 

