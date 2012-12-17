from coinpy.lib.database.bsddb_env import BSDDBEnv
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY
from coinpy.lib.vm.script.standard_script_tools import tx_pubkeyhash_get_address,\
    identify_script, tx_pubkey_get_pubkey
from coinpy.lib.wallet.bsddb.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.lib.bitcoin.address import BitcoinAddress, extract_txout_address
from coinpy.tools.observer import Observable
from coinpy.model.protocol.structures.outpoint import Outpoint
import time
from coinpy.lib.wallet.bsddb.crypter.passphrase import decrypt_masterkey,\
    new_masterkey
from coinpy.tools.crypto.ecdsa.ecdsa_ssl import KEY
from coinpy.lib.wallet.bsddb.crypter.crypter import Crypter
from coinpy.tools.bitcoin.sha256 import doublesha256
from coinpy.model.wallet.wallet_poolkey import WalletPoolKey
from coinpy.model.constants.bitcoin import COIN

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
    
    def __init__(self, wallet_database, runmode):
        super(Wallet, self).__init__()
        self.wallet_database = wallet_database
        self.runmode = runmode
        self.addresses = {}
        self.crypter = Crypter()
        self.plain_masterkeys = []
    
    def open(self):
        self.wallet_database.open()
        self.load()
        
    def create(self, passphrase):
        self.wallet_database.begin_updates()
        crypter = Crypter()
        #first create masterkey
        master_key =  new_masterkey(passphrase)
        plain_masterkey = decrypt_masterkey(master_key, passphrase)
        self.wallet_database.add_master_key(master_key)
        #create transaction pool
        for i in range(100):
            k = KEY()
            k.generate(True)
            public_key = k.get_pubkey()
            crypter.set_key(plain_masterkey, doublesha256(public_key))
            crypted_secret = crypter.encrypt(k.get_secret())
            self.wallet_database.add_crypted_key(public_key, crypted_secret)
            pool_key = WalletPoolKey(i, 60000, time.time(), public_key)
            self.wallet_database.add_poolkey(pool_key)
            
            
        self.wallet_database.commit_updates()
        self.load()
        
    def load(self):
        for public_key, keypair in self.wallet_database.get_keys().iteritems():
            self.addresses[BitcoinAddress.from_publickey(public_key, self.runmode)] = (public_key, False)
        for public_key, secret in self.wallet_database.get_crypted_keys().iteritems():
            self.addresses[BitcoinAddress.from_publickey(public_key, self.runmode)] = (public_key, True)

    def begin_updates(self):
        self.wallet_database.begin_updates()
        
    def commit_updates(self):
        self.wallet_database.commit_updates()
             
    def get_receive_key(self):
        return self.wallet_database.get_receive_key()
        
    def allocate_key(self, public_key, label=None, ischange=False):
        address = BitcoinAddress.from_publickey(public_key, self.runmode) 
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
        yields ( public_key, is_crypted, address, description ) entries.
    """
    def iterkeys(self):
        names = self.wallet_database.get_names()
        for address, (public_key, is_crypted) in self.addresses.iteritems():
            description = self.get_address_description(public_key)
            yield (public_key, is_crypted, address, description)
            
    def get_address_description(self, public_key):
        address = BitcoinAddress.from_publickey(public_key, self.runmode)
        description = ""
        if public_key in self.wallet_database.poolkeys_by_public_key:
            poolkey = self.wallet_database.poolkeys_by_public_key[public_key]
            description = "Pool (id:%d, time:%s)" % (poolkey.poolnum, time.strftime("%Y-%m-%d %H:%m:%S", time.gmtime(poolkey.time)))
        else:
            if address in self.wallet_database.get_names():
                description = "Receive (\"%s\")" % self.wallet_database.get_names()[address].name
            else: 
                description = "Change" 
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
                address = extract_txout_address(txout, self.runmode)
                name = ""
                #print self.get_names()
                #print encode_base58check(chr(ADDRESSVERSION[self.runmode]) + address)
                if address and address in self.get_names():
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


    
    def is_passphrase_required(self, txout):
        address = extract_txout_address(txout, self.runmode)
        _, is_crypted = self.addresses[address]
        return is_crypted
    
    def unlock(self, passphrases):
        for pphrase in passphrases:
            for mkey in self.get_master_keys().values():
                self.plain_masterkeys.append(decrypt_masterkey(mkey, pphrase))
 
    """ Return a private key for a txout as binary bignum. 
    
        Requires unlock() if this key in encrypted  """

    def get_txout_private_key_secret(self, txout):
        address = extract_txout_address(txout, self.runmode)
        public_key, is_crypted = self.addresses[address]
        return self.get_private_key_secret(public_key)
    
    def get_private_key_secret(self, public_key):
        if public_key in self.wallet_database.keys: # private key is not crypted
            k = KEY()
            k.set_privkey(self.wallet_database.keys[public_key].private_key)
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
        address = extract_txout_address(txout, self.runmode)
        if not address: # if unknown script type, return False
            return False
        return self.have_key_for_addresss(address)

    """ Return the wallet's besthash as Uint256() or None if not supported """
    def get_besthash_reference(self):
        locator = self.wallet_database.get_block_locator()
        if locator:
            return self.wallet_database.get_block_locator().highest()
    
    def is_change(self, txout): 
        # Fix to be implemented in main client, see wallet.cpp:390
        # current bad assumption is that any payment to a TX_PUBKEYHASH that
        # is mine but isn't in the address book is change. 
        address = extract_txout_address(txout, self.runmode)
        return self.is_mine(txout) and (address not in self.get_names())
  
    def get_master_keys(self):
        return self.wallet_database.get_master_keys()
    
if __name__ == '__main__':
    from coinpy.model.protocol.runmode import MAIN, TESTNET
    dbenv = BSDDBEnv(r"D:\bitcoin\data\testnet\testnet")
    wallet_db = BSDDBWalletDatabase(dbenv, "wallet.dat")
    wallet = Wallet(wallet_db, TESTNET)
    wallet.open()
    
    for tx, outpoint, txout in wallet.iter_my_outputs():
        print extract_txout_address(txout, TESTNET), (txout.value / COIN)
    #for date, address, name, amount in wallet.iter_transaction_history():
    #    print date, address, name, amount
    #print wallet.get_balance() * 1.0 / COIN 
        
 #   encode_base58check(chr(ADDRESSVERSION[runmode]) + hash160(public_key))