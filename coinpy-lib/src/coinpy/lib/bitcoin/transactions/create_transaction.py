from coinpy.model.protocol.structures.tx import Tx
from coinpy.model.protocol.structures.tx_out import TxOut
from coinpy.lib.script.script_pubkeyhash import make_script_pubkeyhash
from coinpy.model.protocol.structures.tx_in import TxIn
from coinpy.model.scripts.script import Script
from coinpy.lib.bitcoin.transactions.sign_transaction import sign_transaction

"""
    output_list: list of (Outpoint, TxOut) tuples
    address: 20byte bytestring address 
    change_adress: 20byte bytestring address 
    amount: value in COINS.
    fee: value in COINS.
"""
def create_pubkeyhash_transaction(output_list, address, change_adress, amount, fee):
    amount_in = sum(txout.value for outpoint, txout in output_list) 
    amount_change = int(amount_in - amount - fee)
    #assert amount_change > 0
    in_list = [TxIn(previous_output=outpoint, script=Script([])) for outpoint, txout in output_list]
    out_list = [TxOut(value=amount, script=make_script_pubkeyhash(address)),
                TxOut(value=amount_change, script=make_script_pubkeyhash(change_adress))]
    return Tx(version=1, in_list=in_list, out_list=out_list, locktime=0)
        
if __name__ == '__main__':
    #n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo
    from coinpy.lib.database.bsddb_env import BSDDBEnv
    from coinpy_tests.mock import Mock
    from coinpy.model.protocol.runmode import MAIN, TESTNET
    from coinpy.lib.bitcoin.wallet.wallet import Wallet
    from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
    from coinpy.lib.bitcoin.wallet.coin_selector import CoinSelector
    from coinpy.tools.bitcoin.base58check import decode_base58check
    from coinpy.model.constants.bitcoin import COIN
    from coinpy.lib.vm.vm import TxValidationVM

    import os
    
    runmode = TESTNET
    wallet_filename= "D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\wallet_testnet.dat"
    directory, filename = os.path.split(wallet_filename)
    bsddb_env = BSDDBEnv(directory)
    wallet = Wallet(None, BSDDBWalletDatabase(bsddb_env, filename), runmode)
    
    selector = CoinSelector()
    amount, fee = 145.0065*COIN, 0*COIN
    #list of (txhash, tx, index, txout)
    outputs = list(wallet.iter_my_outputs())
    selected_outputs = selector.select_coins(outputs, amount + fee)
    tx = create_pubkeyhash_transaction(selected_outputs, 
                                        decode_base58check("n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo"), 
                                        decode_base58check("n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo"), 
                                        amount, 
                                        fee)
    sign_transaction(tx, selected_outputs)
    vm = TxValidationVM()
    print tx
    print len(selected_outputs)
    print vm.validate(tx, 0, selected_outputs[0].txout.script, tx.in_list[0].script)
    print vm.validate(tx, 1, selected_outputs[1].txout.script, tx.in_list[1].script)
    print vm.validate(tx, 2, selected_outputs[2].txout.script, tx.in_list[2].script)
