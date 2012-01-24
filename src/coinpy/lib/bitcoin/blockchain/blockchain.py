# -*- coding:utf-8 -*-
"""
Created on 24 Jan 2012

@author: kris
"""
from coinpy.lib.bitcoin.blockchain.blockchain_constraints import BlockchainConstraints
from coinpy.lib.bitcoin.blockchain.branch_reorganize import BranchReorganize
from coinpy.lib.bitcoin.blockchain.blockchain_updater import BlockchainUpdater

class Blockchain():
    def __init__(self, database):
        self.database = database
        self.contraints = BlockchainConstraints(self.txverifier)
        
    def appendblock(self, blockhash, block):
        updater = BlockchainUpdater(self.database, self.contraints)  
        reorg = self.reorganize_on_appendblock(blockhash, block)
        if (reorg):
            updater.reorganise_mainbranch(reorg)
        updater.mainchain_appendblock(blockhash, block)      
        updater.commit()
        
    def reorganize_on_appendblock(self, blockhash, block):
        brprev = self.database.get_branch(block.blockheader.hash_prev)
        if not brprev.is_mainchain():
            mainchain_parent = brprev.mainchain_parent()
            altchain = self.database.get_branch(mainchain_parent, brprev)
            mainchain = self.database.get_branch(mainchain_parent, self.indexdb.hashbestchain())
            if (altchain.work() + block.blockheader.work() > mainchain.work()):
                return BranchReorganize(altchain, mainchain)
        return (None)
