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


## signs: 'tx.in_list' with the keys in 'controlled_output_list' 
#   'tx.in_list' and 'controlled_output_list'  they must be of the same 
#   length and must be given in the same order)
def sign_transaction(tx, controlled_output_list):
    #Sign the current transaction 
    result_scripts = []
    for input, output in zip(tx.in_list, controlled_output_list):
        script_save = input.script
        input.script = output.txout.script
        #Serialize and append hash type
        enctx = TxSerializer().serialize(tx) + b"\x01\x00\x00\x00"
        #Get hash 
        hash = doublesha256(enctx)
        key = KEY()
        key.set_privkey(output.keypair.private_key)
        signature = key.sign(hash) + "\x01" # append hash_type SIGHASH_ALL
        script_type = identify_script(output.txout.script)
        # if unknown script type, return None
        result = None
        if script_type == TX_PUBKEYHASH:
            result = make_script_pubkeyhash_sig(output.keypair.public_key, signature)
        if script_type == TX_PUBKEY:
            result =  make_script_pubkey_sig(signature)
        result_scripts.append(result)
        input.script = script_save
    #Set all signature 
    for input, scriptsig in zip(tx.in_list, result_scripts):
        input.script = scriptsig
