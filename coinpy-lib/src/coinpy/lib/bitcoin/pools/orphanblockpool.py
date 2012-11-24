from coinpy.tools.observer import Observable

""" OrphanBlockPool """
class OrphanBlockPool(Observable):
    EVT_ADDED_ORPHAN_BLOCK = Observable.createevent()
    EVT_REMOVED_ORPHAN_BLOCK = Observable.createevent()

    def __init__(self, log):
        Observable.__init__(self)
        self.log = log
        self.blocks = {}
        self.blocks_by_prev = {} # { prevhash => [blkhash1, blkhash2, ...], ...}
        
    def __contains__(self, hash):  
        return hash in self.blocks
    
    def contains_block(self, blkhash):
        return hash in self.blocks
    
    def add_block(self, sender, hash, block):
        self.blocks[hash] = (sender, hash, block)
        if block.blockheader.hash_prev not in self.blocks_by_prev:
            self.blocks_by_prev[block.blockheader.hash_prev] = []
        self.blocks_by_prev[block.blockheader.hash_prev].append(hash)
        self.fire(self.EVT_ADDED_ORPHAN_BLOCK, hash=hash)
        
    def get_block(self, blkhash):
        return self.blocks[blkhash]

    def contains(self, blkhash):
        return blkhash in self.blocks


    def get_orphan_root(self, blkhash):
        while blkhash in self.blocks:
            sender, hash, block = self.blocks[blkhash]
            blkhash = block.blockheader.hash_prev
        return (sender, hash)

    def pop_descendant_blocks(self, blkhash):
        result = []
        workqueue = [blkhash]
        while workqueue:
            blkhash = workqueue.pop()
            if blkhash in self.blocks_by_prev:
                result += [self.blocks[h] for h in self.blocks_by_prev[blkhash]]
                workqueue += self.blocks_by_prev[blkhash]
                del self.blocks_by_prev[blkhash]
        for sender, hash, block in result:
            del self.blocks[hash]
            self.fire(self.EVT_REMOVED_ORPHAN_BLOCK, hash=hash)
        return result
'''

    // Recursively process any orphan blocks that depended on this one
    vector<uint256> vWorkQueue;
    vWorkQueue.push_back(hash);
    for (int i = 0; i < vWorkQueue.size(); i++)
    {
        uint256 hashPrev = vWorkQueue[i];
        for (multimap<uint256, CBlock*>::iterator mi = mapOrphanBlocksByPrev.lower_bound(hashPrev);
             mi != mapOrphanBlocksByPrev.upper_bound(hashPrev);
             ++mi)
        {
            CBlock* pblockOrphan = (*mi).second;
            if (pblockOrphan->AcceptBlock())
                vWorkQueue.push_back(pblockOrphan->GetHash());
            mapOrphanBlocks.erase(pblockOrphan->GetHash());
            delete pblockOrphan;
        }
        mapOrphanBlocksByPrev.erase(hashPrev);
    }
'''