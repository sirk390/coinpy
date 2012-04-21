# -*- coding:utf-8 -*-
"""
Created on 6 Mar 2012

@author: kris
"""
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.lib.script.script_pubkeyhash import make_script_pubkeyhash_sig
from coinpy.tools.crypto.ecdsa.ecdsa_ssl import KEY
from coinpy.lib.script.standard_script_tools import identify_script
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY
from coinpy.lib.script.script_pubkey import make_script_pubkey_sig

""""""
def sign_transaction(tx, txout_list, secret_list):
    #Sign the current transaction 
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
