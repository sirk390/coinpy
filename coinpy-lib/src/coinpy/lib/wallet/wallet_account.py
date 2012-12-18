from coinpy.model.constants.bitcoin import COINBASE_MATURITY,\
    CONFIRMATIONS
from coinpy.lib.transactions.address import BitcoinAddress
from coinpy.tools.bitcoin.base58check import decode_base58check
from coinpy.tools.observer import Observable
from coinpy.lib.wallet.coin_selector import CoinSelector
from coinpy.lib.transactions.create_transaction import create_pubkeyhash_transaction
from coinpy.lib.transactions.sign_transaction import sign_transaction
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.model.protocol.structures.merkle_tx import MerkleTx
from coinpy.lib.transactions.create_wallet_tx import create_wallet_tx
from coinpy.lib.transactions.hash_tx import hash_tx
import time
import random
from coinpy.model.planned_transaction import PlannedTransaction
from coinpy.lib.wallet.wallet import KeyDecryptException
from coinpy.tools.reactor.reactor import reactor


class WalletAccount(Observable):
    EVT_BALANCE_CHANGED = Observable.createevent() 
    EVT_PUBLISH_TRANSACTION = Observable.createevent() 
    EVT_NEW_TRANSACTION_ITEM = Observable.createevent() 
    EVT_CONFIRMED_TRANSACTION_ITEM = Observable.createevent() 
    EVT_NEW_ADDRESS_DESCRIPTION = Observable.createevent() 

    def __init__(self, log, name, wallet, blockchain):
        super(WalletAccount, self).__init__()
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
        - status_unknown : True if no BlockLocator() was found in the wallet.
        - is_blockchain_synched : only valid if not status_unknown, True if the blockchain is height is greater than the wallet height.
        - confirmed_outputs : 
        - unconfirmed_outputs : 
        - confirmed_transactions : 
        - unconfirmed_transactions :
    '''
    def compute_balances(self):
        #improvement: could only check if all my transactions are present in the blockchain
        wallet_besthash = self.wallet.get_besthash_reference()
        self.status_unknown = not wallet_besthash
        if not self.status_unknown:
            self.is_blockchain_synched = self.blockchain.contains_block(wallet_besthash)
        
        #fillin confirmed/unconfirmed outputs (allows to compute the balance)
        self.confirmed_outputs = []
        self.unconfirmed_outputs = []
        for tx, outpoint, txout in self.wallet.iter_my_outputs():
            confirmed = False
            if (self.blockchain.contains_transaction(outpoint.hash) and
                self.blockchain.get_transaction_handle(outpoint.hash).get_block().is_mainchain()):
                height = self.blockchain.get_transaction_handle(outpoint.hash).get_block().get_height()
                confirmed = self.is_confirmed(tx, height)
            if confirmed:
                self.confirmed_outputs.append([tx, txout])
            else:
                self.unconfirmed_outputs.append([tx, txout])
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
                self.fire(self.EVT_CONFIRMED_TRANSACTION_ITEM, item=(txhash,))
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
        reactor.call_later(seconds, self.republish_transactions)

    def get_receive_address(self):
        public_key = self.wallet.get_receive_key()
        return BitcoinAddress.from_publickey(public_key, self.wallet.runmode)
    
    def set_receive_label(self, address_base58, label):
        address = BitcoinAddress.from_base58addr(address_base58)
        self.wallet.begin_updates()
        public_key, is_crypted = self.wallet.addresses[address] #decode_base58check(address)[1:]
        self.wallet.allocate_key(public_key, label)
        self.wallet.commit_updates()
        
        new_description = self.wallet.get_address_description(public_key)
        self.fire(self.EVT_NEW_ADDRESS_DESCRIPTION, public_key=public_key, description=new_description)

    """
    
        amount: value in COIN.
    """
    def create_transaction(self, amount, address, fee):
        outputs = [(outpoint, txout) for (tx, outpoint, txout) in self.iter_my_outputs()]
        selected_outputs = self.coin_selector.select_coins(outputs, (amount + fee))
        
        change_public_key = self.wallet.get_receive_key()
        change_address = BitcoinAddress.from_publickey(change_public_key, self.wallet.runmode)
        tx = create_pubkeyhash_transaction(selected_outputs, 
                                        address.get_hash160(), #decode_base58check(address)[1:],  #remove ADDRESSVERSION[runmode] byte
                                        change_address.get_hash160(), #decode_base58check(change_address)[1:],  #remove ADDRESSVERSION[runmode] byte
                                        amount, 
                                        fee)
        return (PlannedTransaction(selected_outputs, amount, address, change_public_key, change_address, fee, tx))        
    
    def is_passphrase_required(self, planned_transaction):
        for outpoint, txout in planned_transaction.selected_outputs:
            if self.wallet.is_passphrase_required(txout):
                return True
        return False
    
    def send_transaction(self, planned_tx, passphrases):
        try:
            self.wallet.unlock(passphrases)
            privkey_list = []
            for outpoint, txout in planned_tx.selected_outputs:
                privkey_list.append(self.wallet.get_txout_private_key_secret(txout))
        finally:
            self.wallet.lock()
        sign_transaction(planned_tx.tx, 
                              [txout for outpoint, txout in planned_tx.selected_outputs], 
                              privkey_list)
        txhash = hash_tx(planned_tx.tx)
        self.log.info("Sending %f to %s (fee:%f), change address: %s, hash:%s" % (planned_tx.amount, str(planned_tx.address), planned_tx.fee, str(planned_tx.change_address), str(txhash)))
        #Initially, create an empty MerkleTx (the tx is not yet in a block)
        merkle_tx = MerkleTx(planned_tx.tx, 
                             Uint256.zero(), 
                             [], 
                             4294967295)
        self.wallet.begin_updates()
        self.wallet.allocate_key(planned_tx.change_public_key, ischange=True)
        #Set the spend flags for the input transactions
        for outpoint, txout in planned_tx.selected_outputs:
            input_wallet_tx = self.wallet.get_transaction(outpoint.hash)
            input_wallet_tx.set_spent(outpoint.index)
            self.wallet.set_transaction(outpoint.hash, input_wallet_tx)
        #Add the wallet_tx (contains supporting transations)
        txtime = int(time.time())
        wallet_tx = create_wallet_tx(self.blockchain, merkle_tx, txtime)
        self.wallet.add_transaction(txhash, wallet_tx)
        self.wallet.commit_updates()
        self.fire(self.EVT_NEW_TRANSACTION_ITEM, item=(planned_tx.tx, txhash, txtime, planned_tx.address, "", -planned_tx.amount, False))
        
        self.compute_balances()# we could only compute delta here
        self.fire(self.EVT_PUBLISH_TRANSACTION, txhash=txhash, tx=planned_tx.tx)
        self.last_tx_publish[txhash] = txtime
        #update description of change address
        new_description = self.wallet.get_address_description(planned_tx.change_public_key)
        self.fire(self.EVT_NEW_ADDRESS_DESCRIPTION, public_key=planned_tx.change_public_key, description=new_description)

if __name__ == '__main__':
   pass