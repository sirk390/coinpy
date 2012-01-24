# -*- coding:utf-8 -*-
"""
Created on 24 Jan 2012

@author: kris
"""
from coinpy.model.constants.bitcoin import COINBASE_MATURITY
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.lib.vm.vm import TxValidationVM

class BlockchainLogic():
    def __init__(self):
        self.vm = TxValidationVM()
        
    def on_disconnect_block(self, blockchain, block):
        for tx in block.transactions:
            for txin in tx.in_list:
                tx = blockchain.get_transaction(txin.previous_output.hash)
                tx.mark_spent(txin.prevout.n, False)

    def on_connect_block(self, blockchain, block, blockheight):
        for tx in block.transactions:
            txhash = hash_tx(tx)
            for index, txin in enumerate(tx.in_list):
                #fetch inputs
                itf_txprev = blockchain.get_transaction(txin.previous_output.hash)
                txprev = itf_txprev.get_transaction()
                #check matured coinbase.
                if (txprev.iscoinbase()):
                    blockprev = txprev.get_block()
                    if (blockheight - blockprev.height < COINBASE_MATURITY):
                        raise Exception("#trying to spend unmatured coins.")
                #verify scripts
                if not self.vm.validate(tx, index, txprev.out_list[txin.previous_output.index].script, tx.in_list[index].script):
                    raise Exception("input scritp/signature validation failed")
                #check double-spend
                if (itf_txprev.is_output_spent(txin.prevout.n)):
                    raise Exception( "output allready spent")
                #mark spent
                itf_txprev.mark_spent(txin.prevout.n, True, txhash)
            
  