
class DbTxIndex():
    """
        version: bitcoin version (e.g. 32200)
        pos (DiskTxPos): Position of the transation om disk
        spent (list of DiskTxPos): locations of spending transactions (equal to DiskTxPos.null() if not spend) 
    """
    def __init__(self, version, pos, spent):
        self.version, self.pos, self.spent  = version, pos, spent
     
    def is_output_spent(self, output):
        #when spent, CDiskTxPos.File is set to -1, main.h:135 IsNull() 
        return (self.txindex.spent[output].file == -1)
    
    def __eq__(self, other):
        return (self.version == other.version and
                self.pos == other.pos and
                self.spent == other.spent)
        
    def __str__(self):
        return ("DbTxIndex(ver:%d,pos:%s,spent(%d):[%s...])" % 
                    (self.version, 
                     str(self.pos), 
                     len(self.spent), 
                     ",".join([str(i) for i in self.spent[0:5]])))
