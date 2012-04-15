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
import random


class WalletAccount(Observable):
    EVT_BALANCE_CHANGED = Observable.createevent() 
    EVT_PUBLISH_TRANSACTION = Observable.createevent() 
    EVT_NEW_TRANSACTION_ITEM = Observable.createevent() 
    EVT_CONFIRMED_TRANSACTION_ITEM = Observable.createevent() 

    def __init__(self, reactor, log, name, wallet, blockchain):
        super(WalletAccount, self).__init__(reactor)
        self.name = name
        self.wallet = wallet
        self.blockchain = blockchain
        self.blockchain.subscribe(blockchain.EVT_NEW_HIGHEST_BLOCK, self.on_new_highest_block)
        self.log = log
        self.lastblock_time = 0
        self.last_tx_publish = {}
        self.confirmed_outputs = []
        self.unconfirmed_outputs = []
        self.confirmed_transactions = {}
        self.unconfirmed_transactions = {}
       
        #Satoshi wallet format doesn't store confirmations so we have 
        #to recompute confirmations every time.
        self.blockchain_height = self.blockchain.get_height()
        self.compute_balances()
    
        self.coin_selector = CoinSelector()
        self.schedule_republish_transactions()
        
        
    '''
     
    Set the followings attributes:
        - is_blockchain_synched : True if the blockchain is height is greater than the wallet height.
        - confirmed_outputs : 
        - unconfirmed_outputs : 
        - confirmed_transactions : 
        - unconfirmed_transactions :
    '''
    def compute_balances(self):
        #improvement: could only check if all my transactions are present in the blockchain
        self.is_blockchain_synched = self.blockchain.contains_block(self.get_besthash())
        
        #fillin confirmed/unconfirmed outputs (allows to compute the balance)
        self.confirmed_outputs = []
        self.unconfirmed_outputs = []
        for output in self.wallet.iter_my_outputs():
            confirmed = False
            if (self.blockchain.contains_transaction(output.txhash) and
                self.blockchain.get_transaction_handle(output.txhash).get_block().is_mainchain()):
                height = self.blockchain.get_transaction_handle(output.txhash).get_block().get_height()
                confirmed = self.is_confirmed(output.tx, height)
            if confirmed:
                self.confirmed_outputs.append([output.tx, output.txout])
            else:
                self.unconfirmed_outputs.append([output.tx, output.txout])
        confirmed_transactions = {}
        unconfirmed_transactions = {}
        #compute the balance
        self.unconfirmed_balance = sum(txout.value for tx, txout in self.unconfirmed_outputs)
        self.confirmed_balance = sum(txout.value for tx, txout in self.confirmed_outputs)
        self.fire(self.EVT_BALANCE_CHANGED, confirmed=self.confirmed_balance, unconfirmed=self.unconfirmed_balance, height=self.blockchain_height)

        #fillin confirmed/unconfirmed outputs transactions (for history and confirmations)
        for wallet_tx, hash, date, address, name, amount in self.wallet.iter_transaction_history():
            confirmed = False
            if self.blockchain.contains_transaction(hash):
                height = self.blockchain.get_transaction_handle(hash).get_block().get_height()
                confirmed = self.is_confirmed(wallet_tx.merkle_tx.tx, height)
            if (confirmed):
                confirmed_transactions[hash] = [wallet_tx, hash, date, address, name, amount]
            else:
                unconfirmed_transactions[hash] = [wallet_tx, hash, date, address, name, amount]
                self.last_tx_publish[hash] = 0
        #send newly confirmed transaction events
        for txhash in self.unconfirmed_transactions:
            if txhash in confirmed_transactions:
                self.fire(self.EVT_CONFIRMED_TRANSACTION_ITEM, item=(txhash))
        self.confirmed_transactions = confirmed_transactions
        self.unconfirmed_transactions = unconfirmed_transactions
    
    def iter_my_outputs(self):
        return self.wallet.iter_my_outputs()
    
    def iter_transaction_history(self):
        for wallet_tx, hash, date, address, name, amount in self.confirmed_transactions.values():
            yield (wallet_tx, hash, date, address, name, amount, True)
        for wallet_tx, hash, date, address, name, amount in self.unconfirmed_transactions.values():
            yield (wallet_tx, hash, date, address, name, amount, False)
    
    '''Return the confirmed account balance.
    
     Return the received coins seen in mainchain at a depth of minimum 6
     and the minted coins in mainchain at a depth of COINBASE_MATURITY.
    '''
    def get_confirmed_balance(self):
        return self.confirmed_balance
    
    '''Return the unconfirmed account balance.
     
    Return the coins not seen in mainchain, the coins seen in mainchain
    with a depth < 6, and the coins minted whith a depth < COINBASE_MATURITY.
    '''
    def get_unconfirmed_balance(self):
        return self.unconfirmed_balance
    
    def get_blockchain_height(self):
        return self.blockchain_height

    def is_confirmed(self, tx, height):
        if tx.iscoinbase():
            return (self.blockchain_height >  height + COINBASE_MATURITY)
        return (self.blockchain_height >  height + CONFIRMATIONS)
        
    def on_new_highest_block(self, event):
        self.blockchain_height = event.height
        self.lastblock_time = time.time()
        self.compute_balances()

    def get_besthash(self): 
        return self.wallet.get_besthash_reference()
    
    """
         Do this infrequently and randomly to avoid giving away
         that these are our transactions.
    """
    def republish_transactions(self):
        tnow = time.time()
        for wallet_tx, txhash, date, address, name, amount in self.unconfirmed_transactions.values():
            # Only if at least one block was received more than 5min after last publishing.
            if (self.lastblock_time > self.last_tx_publish[txhash] + 5*60):
                self.fire(self.EVT_PUBLISH_TRANSACTION, txhash=txhash, tx=wallet_tx.merkle_tx.tx)
                self.last_tx_publish[hash] = tnow
        self.schedule_republish_transactions()
        
    """"""
    def schedule_republish_transactions(self):
        seconds = random.randint(5*60, 30*60)
        self.reactor.schedule_later(seconds, self.republish_transactions)

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
        sign_transaction(tx, selected_outputs)
        txhash = hash_tx(tx)
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
        self.fire(self.EVT_NEW_TRANSACTION_ITEM, item=(tx, txhash, txtime, address, "", -amount, False))
        
        self.compute_balances()# we could only compute delta here
        self.fire(self.EVT_PUBLISH_TRANSACTION, txhash=txhash, tx=tx)
        self.last_tx_publish[txhash] = txtime
        
if __name__ == '__main__':
   pass