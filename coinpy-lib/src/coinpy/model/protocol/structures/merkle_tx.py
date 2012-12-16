class MerkleTx():
    """ A transaction with a merkle branch linking it to the blockchain
    
        tx (Tx): transaction
        blockhash (Uint256) 
        merkle_branch (list of Uint256) 
        nindex (int) 
    """
    def __init__(self, tx, blockhash, merkle_branch, nindex):
        self.tx = tx
        self.blockhash = blockhash
        self.merkle_branch = merkle_branch
        self.nindex = nindex

    def __eq__(self, other):
        return (self.tx == other.tx and 
                self.blockhash == other.blockhash and
                self.merkle_branch == other.merkle_branch and
                self.nindex == other.nindex)
         
    def __str__(self):
        return ("MerkleTx(tx:%s, block:%s, merkle_branch(%d):%s..., nindex:%d)" % (str(self.tx), str(self.blockhash), len(self.merkle_branch), ",".join(str(h) for h in self.merkle_branch[:5]), self.nindex))