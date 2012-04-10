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
from coinpy.model.constants.bitcoin import COIN, COINBASE_MATURITY,\
    CONFIRMATIONS
from coinpy.tools.hex import hexstr
from coinpy.lib.bitcoin.address import get_address_from_public_key
from coinpy.model.address_version import ADDRESSVERSION
from coinpy.tools.bitcoin.base58check import encode_base58check,\
    decode_base58check
from coinpy.tools.observer import Observable
from coinpy.model.wallet.controlled_output import ControlledOutput
from coinpy.lib.bitcoin.wallet.coin_selector import CoinSelector
from coinpy.lib.bitcoin.transactions.create_transaction import create_pubkeyhash_transaction
from coinpy.lib.bitcoin.transactions.sign_transaction import sign_transaction
from coinpy.model.protocol.structures.uint256 import uint256
from coinpy.model.protocol.structures.merkle_tx import MerkleTx
from coinpy.lib.bitcoin.transactions.create_wallet_tx import create_wallet_tx
from coinpy.lib.bitcoin.hash_tx import hash_tx
import time


class WalletAccount(Observable):
    EVT_BALANCE_CHANGED = Observable.createevent() 
    EVT_PUBLISH_TRANSACTION = Observable.createevent() 

    EVT_NEW_TRANSACTION_HISTORY_ITEM = Observable.createevent() 

    def __init__(self, reactor, log, name, wallet, blockchain):
        super(WalletAccount, self).__init__(reactor)
        self.name = name
        self.wallet = wallet
        self.blockchain = blockchain
        self.blockchain.subscribe(blockchain.EVT_NEW_HIGHEST_BLOCK, self.on_new_highest_block)
        self.log = log
        
        #Satoshi wallet format doesn't store confirmations so we have 
        #to recompute confirmations every time.
        self.blockchain_height = self.blockchain.get_height()
        self.check_blockchain_synch()
        self._recompute_balance()
    
        self.coin_selector = CoinSelector()
    '''Determine if the blockchain has at least the height of the wallet.
     
    Set the followings attributes:
        - is_blockchain_synched : True if the blockchain is height is greater than the wallet height.
        - mainchain_outputs : outputs that are present in the blockchain and are controlled by me.
        - other_outputs : outputs that are not present in the blockchain and are controlled by me.
    '''
    def check_blockchain_synch(self):
        #improvement: could only check if all my transactions are present in the blockchain
        self.is_blockchain_synched = self.blockchain.contains_block(self.get_besthash())
        if self.is_blockchain_synched:
            self.mainchain_outputs = []
            self.other_outputs = []
            for output in self.wallet.iter_my_outputs():
                if (self.blockchain.contains_transaction(output.txhash) and
                    self.blockchain.get_transaction_handle(output.txhash).get_block().is_mainchain()):
                    height = self.blockchain.get_transaction_handle(output.txhash).get_block().get_height()
                    self.mainchain_outputs.append([height, output.tx, output.txout])
                else:
                    self.other_outputs.append([output.tx, output.txout])
                   
        
    def iter_my_outputs(self):
        return self.wallet.iter_my_outputs()
    
    def iter_transaction_history(self):
        for tx, hash, date, address, name, amount in self.wallet.iter_transaction_history():
            if self.blockchain.contains_transaction(hash):
                height = self.blockchain.get_transaction_handle(hash).get_block().get_height()
                confirmed = self.is_confirmed(tx, height)
            else:
                confirmed = False
            yield (tx, hash, date, address, name, amount, confirmed)
        
    def iter_unconfirmed_transactions(self):
        return self.wallet.iter_unconfirmed_transactions()
    
    '''Return the confirmed account balance.
     
    Return 0 if the mainchain is not synchronized (the blockchain height is 
    lower than the wallet height).
    Otherwise, return the received coins seen in mainchain at a depth of minimum 6
     + the minted coins in mainchain at a depth of COINBASE_MATURITY.
    '''
    def get_confirmed_balance(self):
        return self.confirmed_balance
    
    '''Return the unconfirmed account balance.
     
    Return the sum of all outputs if the mainchain is not synchronized.
    Otherwise, return the coins seen in mainchain with a depth < 6, and the coins
    minted whith a depth < COINBASE_MATURITY
    '''
    def get_unconfirmed_balance(self):
        return self.unconfirmed_balance
    
    def get_blockchain_height(self):
        return self.blockchain_height

    def is_confirmed(self, tx, height):
        if tx.iscoinbase():
            return (self.blockchain_height >  height + COINBASE_MATURITY)
        return (self.blockchain_height >  height + CONFIRMATIONS)
        
    def _recompute_balance(self):
        confirmed, unconfirmed = 0, 0
        if not self.is_blockchain_synched:
            #SPEED UP: can be done only once
            for output in self.wallet.iter_my_outputs():
                unconfirmed += output.txout.value
        else:  
            for height, tx, txout in self.mainchain_outputs:
                if self.is_confirmed(tx, height):
                    confirmed += txout.value
                else:
                    unconfirmed += txout.value
            for tx, txout in self.other_outputs:
                unconfirmed += txout.value
        self.confirmed_balance = confirmed
        self.unconfirmed_balance = unconfirmed
        self.fire(self.EVT_BALANCE_CHANGED, confirmed=self.confirmed_balance, unconfirmed=self.unconfirmed_balance, height=self.blockchain_height)

    def on_new_highest_block(self, event):
        self.blockchain_height = event.height
        self.check_blockchain_synch()
        self._recompute_balance()

    def get_besthash(self): 
        return self.wallet.get_besthash_reference()
    """
    
        amount: value in COIN.
    """
    def send_transaction(self, amount, address, fee):
        outputs = list(self.iter_my_outputs())
        selected_outputs = self.coin_selector.select_coins(outputs, (amount + fee))
        self.wallet.begin_updates() # begin transaction on wallet to allocate a pool_key
        change_keypair = self.wallet.allocate_pool_key()
        change_address = get_address_from_public_key(self.wallet.runmode, change_keypair.public_key)
        tx = create_pubkeyhash_transaction(selected_outputs, 
                                        decode_base58check(address)[1:],  #remove ADDRESSVERSION[runmode] byte
                                        decode_base58check(change_address)[1:],  #remove ADDRESSVERSION[runmode] byte
                                        amount, 
                                        fee)
        txhash = hash_tx(tx)
        sign_transaction(tx, selected_outputs)
        self.log.info("Sending %f to %s (fee:%f), change address: %s, hash:%s" % (amount, address, fee, change_address, str(txhash)))
        #Initially, create an empty MerkleTx (the tx is not yet in a block)
        merkle_tx = MerkleTx(tx, 
                             uint256.zero(), 
                             [], 
                             4294967295)
        #Set the spend flags for the input transactions
        for output in selected_outputs:
            input_wallet_tx = self.wallet.get_transaction(output.txhash)
            input_wallet_tx.set_spent(output.index)
            self.wallet.set_transaction(output.txhash, input_wallet_tx)
        #Add the wallet_tx (contains supporting transations)
        txtime = time.time()
        wallet_tx = create_wallet_tx(self.blockchain, merkle_tx, txtime)
        self.wallet.add_transaction(txhash, wallet_tx)
        self.wallet.commit_updates()
        self.fire(self.EVT_NEW_TRANSACTION_HISTORY_ITEM, item=(tx, txhash, txtime, address, "", amount, False))
        
        self.check_blockchain_synch()# we could only compute delta here
        self._recompute_balance()
        
        
if __name__ == '__main__':
   pass