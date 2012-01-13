# -*- coding:utf-8 -*-
"""
Created on 10 Jan 2012

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_tx import tx_encoder
from coinpy.model.constants.bitcoin import MAX_BLOCK_SIZE, is_money_range
from coinpy.lib.bitcoin.checks.check_error import CheckError
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
        result = self._check_tests([self.check_size_limit,
                                    self.check_vin_empty,
                                    self.check_vout_empty,
                                    self.check_money_range,
                                    self.check_dupplicate_inputs,
                                    self.check_coinbase_script_size,
                                    self.check_null_inputs], 
                                    tx)
        return result
    
    def check_size_limit(self, tx):
        data = self.tx_serializer.encode(tx)
        if len(data) > MAX_BLOCK_SIZE:
            return (CheckError("Transaction too large : %d bytes" % (len(data))))
    
    def check_vin_empty(self, tx):
        if (not tx.in_list):
            return (CheckError("vin empty" ))
        
    def check_vout_empty(self, tx):
        if (not tx.out_list):
            return (CheckError("vout empty" ))
                
    def check_money_range(self, tx):
        for txout in tx.out_list:
            if not is_money_range(txout.value):
                return (CheckError("txout not in money range"))
        if not is_money_range(sum(txout.value for txout in tx.out_list)):
            return (CheckError("txout total not in money range"))

    def check_dupplicate_inputs(self, tx):
        inputs = set()
        for txin in tx.in_list:
            if txin.previous_output in inputs:
                return (CheckError("dupplicate txin"))
            inputs.add(txin.previous_output)

    def check_coinbase_script_size(self, tx):
        if tx.iscoinbase():
            bin_script = self.script_serializer.serialize(tx.in_list[0].script)
            if (len(bin_script) < 2 or len(bin_script) > 100):
                return (CheckError("incorrect coinbase script size : %d" % (len(bin_script))))
            
    def check_null_inputs(self, tx):
        if not tx.iscoinbase():
            for txin in tx.in_list:
                if (txin.previous_output.is_null()):
                    return (CheckError("null prevout"))

    # test helper aggregate function
    def _check_tests(self, methods, *args):
        for m in methods:
            result = m(*args)
            if result:
                return (result)
        return None
                
        