class DbBlockIndex():
    """
        version (int): e.g. 32200
        hash_next (Uint256): hash of the next block in the mainchai n(null if best)
        file (int): file number that contains the block (e.g. 1 for "blk0001.dat", 2 for "blk0002.dat"...).
        blockpos (int): position in the "blk{NNNN}.dat" file.
        height (int): height in the blockchain
        blockheader (BlockHeader): blockheader.
    """
    def __init__(self, version, hash_next, file, blockpos, height, blockheader):
        self.version = version
        self.hash_next = hash_next
        self.file = file
        self.blockpos = blockpos 
        self.height = height
        self.blockheader = blockheader
    
    def __eq__(self, other):
        return (self.version == other.version and
                self.hash_next == other.hash_next and 
                self.file == other.file and 
                self.blockpos == other.blockpos and 
                self.height == other.height and 
                self.blockheader == other.blockheader)

    def __str__(self):
        return ("DbBlockIndex(version:%d,hash_next:%s,file:%s,blockpos:%d,height:%d,blockheader:%s)" % 
                    (self.version, 
                     self.hash_next, 
                     self.file,
                     self.blockpos, 
                     self.height,
                     self.blockheader))
