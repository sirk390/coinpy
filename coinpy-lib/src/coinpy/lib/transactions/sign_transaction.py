from coinpy.lib.serialization.structures.s11n_tx import TxSerializer
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.tools.crypto.ecdsa.ecdsa_ssl import KEY
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY
from coinpy.model.scripts.script import Script
from coinpy.lib.vm.script.standard_scripts import make_script_pubkeyhash_sig,\
    make_script_pubkey_sig
from coinpy.lib.vm.script.identify_scripts import identify_script

def sign_transaction_input(tx, input_index, txout_script, intput_script_type, secret):
    # Set all txin to empty
    txin_scripts_save = [txin.script for txin in tx.in_list]
    for txin in tx.in_list:
        txin.script = Script([])
    # Set the current input script to the outpoint's script value
    tx.in_list[input_index].script = txout_script
    # Serialize and append hash type
    enctx = TxSerializer().serialize(tx) + b"\x01\x00\x00\x00"
    # Get hash and Sign
    txhash = doublesha256(enctx)
    key = KEY()
    key.set_secret(secret)
    signature = key.sign(txhash) + "\x01" # append hash_type SIGHASH_ALL
    # Restore Txin scripts
    for txin, script_save in zip(tx.in_list, txin_scripts_save):
        txin.script = script_save
    # Set the signed script
    if intput_script_type == TX_PUBKEYHASH:
        tx.in_list[input_index].script = make_script_pubkeyhash_sig(key.get_pubkey(), signature)
    if intput_script_type == TX_PUBKEY:
        tx.in_list[input_index].script = make_script_pubkey_sig(signature)

def sign_transaction(tx, txout_list, secret_list):
    for idx, (txout, secret) in enumerate(zip(txout_list, secret_list)):
        input_script_type = identify_script(txout.script)
        sign_transaction_input(tx, idx, txout.script, input_script_type, secret)

def sign_transaction_old(tx, txout_list, secret_list):
    result_scripts = []
    for input, txout, secret in zip(tx.in_list, txout_list, secret_list):
        script_save = input.script
        input.script = txout.script
        #Serialize and append hash type
        enctx = TxSerializer().serialize(tx) + b"\x01\x00\x00\x00"
        #Get hash 
        hash = doublesha256(enctx)
        key = KEY()
        key.set_secret(secret)
        signature = key.sign(hash) + "\x01" # append hash_type SIGHASH_ALL
        script_type = identify_script(txout.script)
        # if unknown script type, return None
        result = None
        if script_type == TX_PUBKEYHASH:
            result = make_script_pubkeyhash_sig(key.get_pubkey(), signature)
        if script_type == TX_PUBKEY:
            result =  make_script_pubkey_sig(signature)
        result_scripts.append(result)
        input.script = script_save
    #Set all signature 
    for input, scriptsig in zip(tx.in_list, result_scripts):
        input.script = scriptsig
