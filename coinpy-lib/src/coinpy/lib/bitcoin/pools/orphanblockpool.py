# -*- coding:utf-8 -*-
"""
Created on 13 Dec 2011

@author: kris
"""

""" OrphanBlockPool """
class OrphanBlockPool():
    def __init__(self, log):
        self.log = log
        self.blocks = {}
        self.blocks_by_prev = {} # { prevhash => [blkhash1, blkhash2, ...], ...}
        
    def __contains__(self, hash):  
        return hash in self.blocks

    def add_block(self, sender, hash, block):
        self.blocks[hash] = (sender, hash, block)
        if block.blockheader.hash_prev not in self.blocks_by_prev:
            self.blocks_by_prev[block.blockheader.hash_prev] = []
        self.blocks_by_prev[block.blockheader.hash_prev].append(hash)
    
    def get_block(self, blkhash):
        return self.blocks[blkhash]

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