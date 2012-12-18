class DbBlockIndex():
    def __init__(self, version, hash_next, file, blockpos, height, blockheader):
        self.version = version
        self.hash_next = hash_next
        self.file = file
        self.blockpos = blockpos 
        self.height = height
        self.blockheader = blockheader
        
    def __str__(self):
        return ("DbBlockIndex(version:%d,hash_next:%s,file:%s,blockpos:%d,height:%d,blockheader:%s)" % 
                    (self.version, 
                     self.hash_next, 
                     self.file,
                     self.blockpos, 
                     self.height,
                     self.blockheader))
