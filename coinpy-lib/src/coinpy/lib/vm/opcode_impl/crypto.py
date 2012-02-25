# -*- coding:utf-8 -*-
"""
Created on 27 Jul 2011

@author: kris
"""
from coinpy.tools.bitcoin.hash160 import hash160
import copy
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.tools.crypto.ecdsa.ecdsa_ssl import KEY
from coinpy.model.scripts.script import Script
from coinpy.lib.vm.stack_valtype import valtype_from_boolean, cast_to_number
from coinpy.lib.vm.opcode_impl.flow import op_verify
from coinpy.lib.serialization.structures.s11n_tx import TxSerializer

def op_hash160(vm, instr):
    if not vm.stack:
        raise Exception("OP_HASH160: Argument required")
    vm.stack[-1] = hash160(vm.stack[-1])

def checksig(vm, sig, pubkey):
    transaction, inputindex, unspent_script = vm.checksig_data
    #Hash type is the last byte of the signature
    hash_type, sig = sig[-1], sig[:-1]
   
    # For performance reasons no full copy is made of the transaction
    # although it would be simpler to understand.
    # e.g. tx_tmp = copy.deepcopy(transaction)
    # The input scripts are saved and then restored.

    #Save input scripts to restore them later
    inscripts = [txin.script for txin in transaction.in_list]
    #Blank out inputs
    #TODO: blank out depending of hash_type (SIGHASH_NONE, SIGHASH_SINGLE, SIGHASH_ANYONECANPAY)
    for txin in transaction.in_list:
        txin.script = Script([])
    #except the current one that is replaced by the unspent_script
    transaction.in_list[inputindex].script =  unspent_script
    #Serialize and append hash type
    enctx = TxSerializer().serialize(transaction) + b"\x01\x00\x00\x00"
    #Get hash 
    hash = doublesha256(enctx)
    #Verify
    key = KEY()
    key.set_pubkey(pubkey)
    #ECDSA_verify: 1 = OK, 0=NOK, -1=ERROR
    result = key.verify(hash, sig) == 1
    #Restore transaction scripts
    for txin, script in zip(transaction.in_list,inscripts):    
        txin.script = script
    return (result)

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
    if len(vm.stack) < pubkey_count:
        raise Exception("OP_CHECKMULTISIG: Stack too small for pubkeys")
    pubkeys = vm.stack[-pubkey_count:]
    del vm.stack[-pubkey_count:]
    if len(vm.stack) < 1:
        raise Exception("OP_CHECKMULTISIG: Stack too small for sig_count")
    sig_count = cast_to_number(vm.stack.pop())
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
