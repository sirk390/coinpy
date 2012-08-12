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
from coinpy.tools.hex import hexstr
from coinpy.model.scripts.hash_types import SIGHASH_ANYONECANPAY, SIGHASH_SINGLE,\
    SIGHASH_MASK, SIGHASH_NONE
from coinpy.model.protocol.structures.tx_out import TxOut
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.opcodes import OP_PUSHDATA
from coinpy.lib.script.push_data import auto_push_data_instruction
from coinpy.model.protocol.structures.tx import Tx
from coinpy.model.protocol.structures.tx_in import TxIn
import hashlib

def op_hash160(vm, instr):
    if not vm.stack:
        raise Exception("OP_HASH160: Argument required")
    vm.stack[-1] = hash160(vm.stack[-1])

def checksig(vm, sig_param, pubkey_param):
    transaction, inputindex, unspent_script = vm.checksig_data
    #Hash type is the last byte of the signature
    hash_type, sig = ord(sig_param[-1]), sig_param[:-1]
    
    # last 5 bits of hash_type : 1=SIGHASH_ALL,2=SIGHASH_NONE, 3=SIGHASH_SINGLE 
    # SIGHASH_ANYONECANPAY = 0x80
    
    # For performance reasons no full copy is made of the transaction
    # although it would be simpler to read.
    # e.g. tx_tmp = copy.deepcopy(transaction)
    # The input scripts are saved and then restored.
    tx_tmp = Tx(transaction.version, 
                [TxIn(txin.previous_output, txin.script, txin.sequence) for txin in transaction.in_list], 
                [TxOut(txout.value, txout.script) for txout in transaction.out_list], 
                transaction.locktime) 
    #Save input scripts to restore them later
    #inlist = transaction.in_list
    #outlist = transaction.out_list
    #inscripts = [txin.script for txin in transaction.in_list]
    #TODO: blank out ouputs depending of hash_type (SIGHASH_NONE, SIGHASH_SINGLE)
    if (hash_type & SIGHASH_MASK == SIGHASH_NONE):
        tx_tmp.out_list = []
    if (hash_type & SIGHASH_MASK == SIGHASH_SINGLE):
        if (inputindex > len(tx_tmp.out_list)):
            raise Exception("OP_CHECKSIG: no corresponding output for input %d using SIGHASH_SINGLE " % (inputindex))
        #n-1 empty TxOuts + original Txout
        tx_tmp.out_list = [TxOut(-1, Script([])) for _ in range(inputindex)] + \
                          [tx_tmp.out_list[inputindex]]
    if (hash_type & SIGHASH_MASK == SIGHASH_SINGLE or 
        hash_type & SIGHASH_MASK == SIGHASH_NONE):
        # let others update at will
        for i in range(len(tx_tmp.in_list)):
            if i != inputindex:
                tx_tmp.in_list[i].sequence = 0
    #blank out other inputs in case of SIGHASH_ANYONECANPAY
    if (hash_type & SIGHASH_ANYONECANPAY):
        tx_tmp.in_list = [tx_tmp.in_list[inputindex]]
        inputindex = 0
    #blank out input scripts
    for txin in tx_tmp.in_list:
        txin.script = Script([])
    #except the current one that is replaced by the signed part (e.g. from the last OP_CODESEPARATOR)
    # of current_script with signature push_data removed
    # note: only 'optimal' push_data instructions with the same signature are removed
    current_script = Script(filter(lambda instr: instr!=auto_push_data_instruction(sig_param),
                            vm.current_script.signed_part().instructions))
    tx_tmp.in_list[inputindex].script = current_script
    #serialize and append hash type
    enctx = TxSerializer().serialize(tx_tmp) + chr(hash_type) + b"\x00\x00\x00"
    
    #print "enctx:", hexstr(enctx)
    #print "sig:", hexstr(sig)
    #print "pubkey:", hexstr(pubkey_param)
    
    #Get hash 
    hash = doublesha256(enctx)
    #Verify
    key = KEY()
    key.set_pubkey(pubkey_param)
    #ECDSA_verify: 1 = OK, 0=NOK, -1=ERROR
    result = key.verify(hash, sig) == 1
    if not result:
        pass
    #Restore transaction scripts
    #for txin, script in zip(inlist,inscripts):    
    #    txin.script = script
    #transaction.in_list = inlist 
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


def op_checkmultisigverify(vm, instr):
    op_checkmultisig(vm, instr)
    op_verify(vm, instr)


"""
OP_SHA1
"""
def op_sha1(vm, instr):
    if (len(vm.stack) < 1):
        raise Exception("OP_SHA1: Missing argument")
    x = vm.stack.pop()
    vm.stack.append(hashlib.sha1(x).digest())
    
"""
OP_SHA256
"""
def op_sha256(vm, instr):
    if (len(vm.stack) < 1):
        raise Exception("OP_SHA256: Missing argument")
    x = vm.stack.pop()
    vm.stack.append(hashlib.sha256(x).digest())
    
"""
OP_RIPEMD160
"""
def op_ripemd160(vm, instr):
    if (len(vm.stack) < 1):
        raise Exception("OP_RIPEMD160: Missing argument")
    x = vm.stack.pop()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(x)
    vm.stack.append(ripemd160.digest())
    
"""
OP_HASH256
"""
def op_hash256(vm, instr):
    if (len(vm.stack) < 1):
        raise Exception("OP_HASH256: Missing argument")
    x = vm.stack.pop()
    vm.stack.append(doublesha256(x))

'''

OP_RIPEMD160 = 166
OP_SHA1 = 167
OP_SHA256 = 168
OP_HASH160 = 169
OP_CODESEPARATOR = 171
OP_CHECKSIG = 172
OP_CHECKSIGVERIFY = 173
OP_CHECKMULTISIG = 174
OP_CHECKMULTISIGVERIFY = 175
'''
