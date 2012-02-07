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
from coinpy.lib.vm.stack_valtype import valtype_from_boolean, cast_to_number
from coinpy.lib.vm.opcode_impl.flow import op_verify

def op_hash160(vm, instr):
    if not vm.stack:
        raise Exception("OP_HASH160: Argument required")
    vm.stack[-1] = hash160(vm.stack[-1])

def checksig(vm, sig, pubkey):
    transaction, inputindex, unspent_script = vm.checksig_data
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
    return (key.verify(hash, sig) == 1)

def check_multisig(vm, sigs, pubkeys):
    while len(sigs) > 0:
        sig = sigs.pop()
        validated = False
        while not validated:
            if len(sigs) > len(pubkeys) - 1:
                return False
            key = pubkeys.pop()
            validated = checksig(vm, sig, key)
    return True

def op_checksig(vm, instr):
    if len(vm.stack) < 2:
        raise Exception("OP_CHECKSIG: Not enough arguments")
    pubkey = vm.stack.pop()
    sig = vm.stack.pop()
    vm.stack.append (valtype_from_boolean(checksig(vm, sig, pubkey) ))

def op_checksigverify(vm, instr):
    op_checksig(vm, instr)
    op_verify(vm, instr)

def op_checkmultisig(vm, instr):
    if len(vm.stack) < 1:
        raise Exception("OP_CHECKMULTISIG: Stack too small for pubkey_count")
    pubkey_count = cast_to_number(vm.stack.pop())
    print "pubkey_count", pubkey_count
    if len(vm.stack) < pubkey_count:
        raise Exception("OP_CHECKMULTISIG: Stack too small for pubkeys")
    pubkeys = vm.stack[-pubkey_count:]
    del vm.stack[-pubkey_count:]
    if len(vm.stack) < 1:
        raise Exception("OP_CHECKMULTISIG: Stack too small for sig_count")
    sig_count = cast_to_number(vm.stack.pop())
    print "sig_count", sig_count
    if len(vm.stack) < sig_count:
        raise Exception("OP_CHECKMULTISIG: Stack too small for sigs")
    sigs = vm.stack[-sig_count:]
    del vm.stack[-sig_count:]
    vm.stack.append (valtype_from_boolean(check_multisig(vm, sigs, pubkeys)))
    
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
