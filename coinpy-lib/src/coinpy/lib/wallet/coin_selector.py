"""Select coins to send from a list of TxOut's.

    Currently selects outputs in the order of arrival
    until the amount is sufficient.
    
    Parameters:
        outputs: list of (Outpoint, TxOut) 
        amount: integer amount in COINS
        
    Return value:
        list of (Outpoint, TxOut) 
        
    Note: The official client minimizes the "change" amount using a 
    stochastic approximation (see subset sum problem) wallet.cpp:893
    It also sends in first priority coins with 1 confirmation mine, 6 others, 
    then 1,1 then 0, 1.
    
    Suggested improvement:
        better anonymity see https://bitcointalk.org/index.php?topic=5559.0
"""
class CoinSelector():
    def select_coins(self, outputs, amount):
        chosen_outputs = []
        amount_found = 0
        for outpoint, txout in outputs:
            if amount_found >= amount:
                return chosen_outputs
            amount_found += txout.value
            chosen_outputs.append((outpoint, txout))
        if amount_found >= amount:
            return chosen_outputs
        raise Exception("not enought funds")

        