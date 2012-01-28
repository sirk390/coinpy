# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.tools.bitcoin.hash160 import hash160
import copy
from coinpy.lib.serialization.messages.s11n_tx import tx_encoder
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.tools.crypto.ecdsa.ecdsa_ssl import KEY
from coinpy.model.scripts.script import Script

def op_hash160(vm, instr):
    if not vm.stack:
        raise Exception("OP_HASH160: Argument required")
    vm.stack[-1] = hash160(vm.stack[-1])

def op_checksig(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_CHECKSIG: Not enough arguments")
    transaction, inputindex, unspent_script = vm.checksig_data
    
    pubkey = vm.stack.pop()
    sig = vm.stack.pop()
    #hash type is the last byte of the signature
    hash_type, sig = sig[-1], sig[:-1]
    #Make a copy of the current transaction
    tx_tmp = copy.deepcopy(transaction)
    #blank out inputs
    for txin in tx_tmp.in_list:
        txin.script = Script([])
    #except the current one that is replaced by the unspent_script
    tx_tmp.in_list[inputindex].script =  unspent_script
    #todo: blank out depending of hash_type (SIGHASH_NONE, SIGHASH_SINGLE, SIGHASH_ANYONECANPAY)
     
    #append hash type
    enctx = tx_encoder().encode(tx_tmp) + b"\x01\x00\x00\x00"
    #get hash 
    hash = doublesha256(enctx)
    #verify
    key = KEY()
    key.set_pubkey(pubkey)
    #ECDSA_verify: 1 = OK, 0=NOK, -1=ERROR
    result = (key.verify(hash, sig) == 1)
    vm.stack.append (result)

'''

OP_RIPEMD160 = 166
OP_SHA1 = 167
OP_SHA256 = 168
OP_HASH160 = 169
OP_HASH256 = 170
OP_CODESEPARATOR = 171
OP_CHECKSIG = 172
OP_CHECKSIGVERIFY = 173
OP_CHECKMULTISIG = 174
OP_CHECKMULTISIGVERIFY = 175
'''
