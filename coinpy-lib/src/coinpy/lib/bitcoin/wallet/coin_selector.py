# -*- coding:utf-8 -*-
"""
Created on 3 Mar 2012

@author: kris
"""


"""CoinSelector allow to use multiple algorithms for selecting coins

    This implementation simply selects outputs in the order of arrival
    until the amount is sufficient.
    Parameters:
        outputs: list of "ControlledOutput" objects
        amount: integer amount in COINS14
    Return value:
        list of selected "ControlledOutput" objects
        
    Note: The official client minimizes the "change" amount using a 
    stochastic approximation (see subset sum problem) wallet.cpp:893
    It also sends in first priority coins with 1 confirmation mine, 6 others, 
    then 1,1 then 0, 1.
    
    Suggested improvement:
        better anonymity see https://bitcointalk.org/index.php?topic=5559.0
"""
class CoinSelector():
    def select_coins(self, outputs, amount):
        chosen_txouts = []
        i, amount_found = 0, 0
        while amount_found < amount:
            if i >= len(outputs):
                raise Exception("not enought funds")
            chosen_txouts.append(outputs[i])
            amount_found += outputs[i].txout.value
            i += 1
        return chosen_txouts    
        
        
        