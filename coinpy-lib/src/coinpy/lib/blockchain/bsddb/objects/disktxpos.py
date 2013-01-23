
NULL_DISKTXPOS=4294967295

class DiskTxPos():
    """Position of a transaction in a storage file (blk{NNNN}.dat)
        
           file(int): file number, NNNN in blk{NNNN}.dat
           blockpos(int): offset in the file of the block containing the transaction
           txpos(int): offset in the file of the transaction
    """
    def __init__(self, file=NULL_DISKTXPOS, blockpos=0, txpos=0):
        self.file, self.blockpos, self.txpos = file, blockpos, txpos
    
    @staticmethod
    def null(self):
        return DiskTxPos(NULL_DISKTXPOS)
    
    def isnull(self):
        #when spent, CDiskTxPos.File is set to -1, main.h:135 IsNull() 
        return (self.file == NULL_DISKTXPOS)
    
    def __eq__(self, other):
        return (self.file == other.file and 
                self.blockpos == other.blockpos and 
                self.txpos == other.txpos)
    
    def setnull(self):
        self.file = NULL_DISKTXPOS
        
    def __str__(self):
        return ("DiskTxPos(file:%d,blockpos:%d,txpos:%d)" % (self.file, self.blockpos, self.txpos))
