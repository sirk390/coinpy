# -*- coding:utf-8 -*-
"""
Created on 13 Feb 2012

@author: kris
"""
from coinpy.lib.database.bsddb_env import BSDDBEnv
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY
from coinpy.lib.script.standard_script_tools import tx_pubkeyhash_get_address,\
    identify_script, tx_pubkey_get_pubkey
from coinpy.tools.bitcoin.hash160 import hash160
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.lib.bitcoin.address import get_address_from_public_key
from coinpy.model.address_version import ADDRESSVERSION
from coinpy.tools.bitcoin.base58check import encode_base58check
from coinpy.tools.observer import Observable
from coinpy.model.wallet.controlled_output import ControlledOutput
from coinpy.model.protocol.structures.outpoint import Outpoint
import time
from coinpy.lib.database.wallet.crypter.passphrase import decrypt_masterkey
from coinpy.tools.crypto.ecdsa.ecdsa_ssl import KEY
from coinpy.lib.database.wallet.crypter.crypter import Crypter
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.tools.hex import hexstr

# Wrong passphrase, missing passphrase, or missing master_key
class KeyDecryptException(Exception):
    pass

'''
    Wallet implementes the basic satoshi wallet logic.
       Database logic is implemented in WalletDatabase
       Features requiring a blockchain are implemented in WalletAccount.
'''
class Wallet(Observable):
    EVT_NEW_TRANSACTION = Observable.createevent()
    
    def __init__(self, reactor, wallet_database, runmode):
        super(Wallet, self).__init__(reactor)
        self.wallet_database = wallet_database
        self.wallet_database.open()
        self.runmode = runmode
        self.addresses = {}
        self.crypter = Crypter()
        self.plain_masterkeys = []

        for public_key, keypair in self.wallet_database.get_keys().iteritems():
            self.addresses[hash160(public_key)] = (public_key, False)
        for public_key, secret in self.wallet_database.get_crypted_keys().iteritems():
            self.addresses[hash160(public_key)] = (public_key, True)
    
    def begin_updates(self):
        self.wallet_database.begin_updates()
        
    def commit_updates(self):
        self.wallet_database.commit_updates()
        
    def get_receive_key(self):
        return self.wallet_database.get_receive_key()
        
    def allocate_key(self, public_key, label=None, ischange=False):
        address = get_address_from_public_key(self.runmode, public_key)
        return self.wallet_database.allocate_key(public_key, address, label)
    
    def add_transaction(self, hashtx, wallet_tx):
        self.wallet_database.set_transaction(hashtx, wallet_tx)

    def get_transaction(self, hashtx):
        return self.wallet_database.get_transaction(hashtx)

    def set_transaction(self, hashtx, wallet_tx):
        self.wallet_database.set_transaction(hashtx, wallet_tx)

    def del_transaction(self, hashtx):
        self.wallet_database.del_transaction(hashtx)

    """
        yields ( public_key, private_key, address, description ) entries.
    """
    def iterkeys(self):
        names = self.wallet_database.get_names()
        for address, (public_key, is_crypted) in self.addresses.iteritems():
            b58addr = encode_base58check(chr(ADDRESSVERSION[self.runmode]) + address)
            description = self.get_address_description(public_key)
            yield (public_key, "", b58addr, description)
            
    def get_address_description(self, public_key):
        address = hash160(public_key)
        description = ""
        if public_key in self.wallet_database.poolkeys_by_public_key:
            poolkey = self.wallet_database.poolkeys_by_public_key[public_key]
            description = "Pool (id:%d, time:%s)" % (poolkey.poolnum, time.strftime("%Y-%m-%d %H:%m:%S", time.gmtime(poolkey.time)))
        else:
            b58addr = encode_base58check(chr(ADDRESSVERSION[self.runmode]) + address)
            if b58addr in self.wallet_database.get_names():
                description = "Receive (\"%s\")" % self.wallet_database.get_names()[b58addr].name
            else: 
                description = "Change" 
        _, is_crypted = self.addresses[address]
        if is_crypted:
            description += "(encrypted)"
        return description
        
    def iter_my_outputs(self):
        for hash, wallet_tx in self.wallet_database.get_wallet_txs().iteritems():
            for index, txout in enumerate(wallet_tx.merkle_tx.tx.out_list):
                if not wallet_tx.is_spent(index) and self.is_mine(txout):
                    yield (wallet_tx.merkle_tx.tx, Outpoint(hash, index), txout)
                    #yield ControlledOutput(hash, wallet_tx.merkle_tx.tx, index, txout, self.get_keypair_for_output(txout))
    ''''
        A TxIn is "debit" if the previous output is in the wallet and is mine.
        If it is, get_debit_txin will return the value spent.
        Debit transaction are used only for transaction history.
        The balance is computed using unspent transactions.
    '''
    def get_debit_txin(self, txin):
        if txin.previous_output.hash not in self.wallet_database.get_wallet_txs():
            return 0
        txprev = self.wallet_database.get_wallet_txs()[txin.previous_output.hash]
        txout = txprev.merkle_tx.tx.out_list[txin.previous_output.index]
        if not self.is_mine(txout):
            return 0
        return txout.value
        
    def get_debit_tx(self, wallet_tx):
        return sum(self.get_debit_txin(txin) for txin  in wallet_tx.merkle_tx.tx.in_list)

    def get_credit_txout(self, txout):
        if self.is_mine(txout):
            return txout.value
        return 0
        
    def get_credit_tx(self, wallet_tx):
        return sum(self.get_credit_txout(txout) for txout  in wallet_tx.merkle_tx.tx.out_list)
     
    def iter_transaction_history(self): # see wallet.cpp:448 GetAmounts
        for hash, wallet_tx in self.wallet_database.get_wallet_txs().iteritems():
            debit = self.get_debit_tx(wallet_tx)
            for txout in wallet_tx.merkle_tx.tx.out_list:
                address = encode_base58check(chr(ADDRESSVERSION[self.runmode]) + self.extract_adress(txout))
                if not address:
                    address = "(unknown)"
                name = ""
                #print self.get_names()
                #print encode_base58check(chr(ADDRESSVERSION[self.runmode]) + address)
                if address in self.get_names():
                    name = self.get_names()[address].name
                if debit > 0 and self.is_change(txout):
                    pass
                elif debit > 0:
                    yield (wallet_tx, hash, wallet_tx.time_received, address, name, -txout.value)
                elif self.is_mine(txout):
                    yield (wallet_tx, hash, wallet_tx.time_received, address, name, txout.value)
          
    def get_wallet_txs(self):
        return self.wallet_database.get_wallet_txs()

    def get_keypairs(self):
        return self.wallet_database.keypairs
    
    def get_poolkeys(self):
        return self.wallet_database.get_poolkeys()
    
    def get_names(self):
        return self.wallet_database.get_names()
    
    def have_key_for_addresss(self, address):
        return (address in self.addresses)

    
    def extract_adress(self, txout):
        script_type = identify_script(txout.script)
        # if unknown script type, return None
        if (script_type is None): 
            return None 
        if script_type == TX_PUBKEYHASH:
            return tx_pubkeyhash_get_address(txout.script)
        if script_type == TX_PUBKEY:
            return hash160(tx_pubkey_get_pubkey(txout.script))
        return None 
    
    def is_passphrase_required(self, txout):
        address = self.extract_adress(txout)
        _, is_crypted = self.addresses[address]
        return is_crypted
    
    def unlock(self, passphrases):
        for pphrase in passphrases:
            for mkey in self.get_master_keys().values():
                self.plain_masterkeys.append(decrypt_masterkey(mkey, pphrase))
 
    """ Return a private key for a txout as binary bignum. 
    
        Requires unlock() if this key in encrypted  """
    def get_private_key_secret(self, txout):
        address = self.extract_adress(txout)
        public_key, is_crypted = self.addresses[address]
        if not is_crypted:
            k = KEY()
            k.set_privkey(self.keypairs[address].private_key)
            return k.get_secret()
        crypted_secret = self.wallet_database.get_crypted_keys()[public_key]
        for key in self.plain_masterkeys:
            self.crypter.set_key(key, doublesha256(public_key))
            secret = self.crypter.decrypt(crypted_secret)
            k = KEY()
            is_compressed = len(public_key) == 33
            k.set_secret(secret, is_compressed)
            if k.get_pubkey() == public_key:
                return secret
        raise KeyDecryptException("Can't decrypt private key, wallet not unlocked or incorrect masterkey")
            
    def lock(self):
        self.plain_masterkeys = []
      
        

    def is_mine(self, txout):
        address = self.extract_adress(txout)
        if not address: # if unknown script type, return False
            return False
        return self.have_key_for_addresss(address)

    def get_besthash_reference(self):
        return self.wallet_database.get_block_locator().highest()
    
    def is_change(self, txout): 
        # Fix to be implemented in main client, see wallet.cpp:390
        # current bad assumption is that any payment to a TX_PUBKEYHASH that
        # is mine but isn't in the address book is change. 
        address = self.extract_adress(txout)
        return self.is_mine(txout) and (address not in self.get_names())
  
    def get_master_keys(self):
        return self.wallet_database.get_master_keys()
    
if __name__ == '__main__':
    from coinpy.model.protocol.runmode import MAIN, TESTNET
    from coinpy.tools.reactor.reactor import Reactor
    dbenv = BSDDBEnv("D:\\repositories\\coinpy\\coinpy-client\\src\\coinpy_client\\data_testnet\\")
    reactor = Reactor()
    wallet_db = BSDDBWalletDatabase(dbenv, "wallet_testnet.dat")
    wallet = Wallet(reactor, wallet_db, TESTNET)
    
    print "\n".join([str(s) for s in wallet.iter_my_outputs()])
    #for date, address, name, amount in wallet.iter_transaction_history():
    #    print date, address, name, amount
    #print wallet.get_balance() * 1.0 / COIN 
        
 #   encode_base58check(chr(ADDRESSVERSION[runmode]) + hash160(public_key))