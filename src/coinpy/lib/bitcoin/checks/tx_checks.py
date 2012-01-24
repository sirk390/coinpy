# -*- coding:utf-8 -*-
"""
Created on 10 Jan 2012

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_tx import tx_encoder
from coinpy.model.constants.bitcoin import MAX_BLOCK_SIZE, is_money_range
from coinpy.lib.serialization.scripts.serialize import ScriptSerializer


class TxVerifier():
    def __init__(self, runmode):
        self.runmode = runmode
        self.tx_serializer = tx_encoder()
        self.script_serializer = ScriptSerializer()
    """
        basic_check: run tests that don't require any context.
    """
    def basic_checks(self, tx):
        self.check_size_limit(tx)
        self.check_vin_empty(tx)
        self.check_vout_empty(tx)
        self.check_money_range(tx)
        self.check_dupplicate_inputs(tx)
        self.check_coinbase_script_size(tx)
        self.check_null_inputs(tx)
    
    def check_size_limit(self, tx):
        data = self.tx_serializer.encode(tx)
        if len(data) > MAX_BLOCK_SIZE:
            raise Exception("Transaction too large : %d bytes" % (len(data)))
    
    def check_vin_empty(self, tx):
        if (not tx.in_list):
            raise Exception("vin empty" )
        
    def check_vout_empty(self, tx):
        if (not tx.out_list):
            raise Exception("vout empty" )
                
    def check_money_range(self, tx):
        for txout in tx.out_list:
            if not is_money_range(txout.value):
                raise Exception("txout not in money range")
        if not is_money_range(sum(txout.value for txout in tx.out_list)):
            raise Exception("txout total not in money range")

    def check_dupplicate_inputs(self, tx):
        inputs = set()
        for txin in tx.in_list:
            if txin.previous_output in inputs:
                raise Exception("dupplicate txin")
            inputs.add(txin.previous_output)

    def check_coinbase_script_size(self, tx):
        if tx.iscoinbase():
            bin_script = self.script_serializer.serialize(tx.in_list[0].script)
            if (len(bin_script) < 2 or len(bin_script) > 100):
                raise Exception("incorrect coinbase script size : %d" % (len(bin_script)))
            
    def check_null_inputs(self, tx):
        if not tx.iscoinbase():
            for txin in tx.in_list:
                if (txin.previous_output.is_null()):
                    raise Exception("null prevout")


        