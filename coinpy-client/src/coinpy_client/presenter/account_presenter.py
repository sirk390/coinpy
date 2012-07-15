# -*- coding:utf-8 -*-
"""
Created on 21 Feb 2012

@author: kris
"""
#wallets
from coinpy.lib.database.wallet.bsddb_wallet_database import BSDDBWalletDatabase
from coinpy.lib.bitcoin.wallet.wallet import Wallet, KeyDecryptException
import os
from coinpy.lib.bitcoin.address import BitcoinAddress
from coinpy.tools.float import is_float
from coinpy.model.constants.bitcoin import COIN
from coinpy.tools.reactor.asynch import asynch_method
import traceback
from coinpy.tools.hex import hexstr
from coinpy_client.view.action_cancelled import ActionCancelledException
 
class AccountPresenter():
    def __init__(self, account, wallet_view, messages_view): 
        self.account = account
        #self.balance = wallet_manager.balance
        self.wallet_view = wallet_view
        self.messages_view = messages_view
        
        self.are_shown_private_keys = False
        
        #show account balance
        for public_key, is_crypted, address, description in  self.account.wallet.iterkeys():
            self.wallet_view.add_key(public_key, public_key, "***", address.to_base58addr(), description)
        wallet_view.balance.set_balance(account.get_confirmed_balance(), account.get_unconfirmed_balance(), account.get_blockchain_height())
        #show transaction history
        for wallet_tx, hash, date, address, name, amount, confirmed in self.account.iter_transaction_history():
            address_str = address and address.to_base58addr() or "(unknown)"
            self.wallet_view.add_transaction_history_item(hash, date, address_str, name, amount, confirmed)
        #listen to balance updates
        self.account.subscribe(self.account.EVT_BALANCE_CHANGED, self.on_balance_changed)
        self.account.subscribe(self.account.EVT_NEW_TRANSACTION_ITEM, self.on_new_transaction_item)
        self.account.subscribe(self.account.EVT_CONFIRMED_TRANSACTION_ITEM, self.on_confirmed_transaction_item)
        self.account.subscribe(self.account.EVT_NEW_ADDRESS_DESCRIPTION, self.on_new_address_description)
                               
        wallet_view.subscribe(wallet_view.EVT_SEND, self.on_send)
        wallet_view.subscribe(wallet_view.EVT_RECEIVE, self.on_receive)
        wallet_view.subscribe(wallet_view.EVT_SHOWHIDE_PRIVATE_KEYS, self.on_show_hide_private_keys)
        
        wallet_view.send_view.subscribe(wallet_view.send_view.EVT_SELECT_VALUE, self.on_select_send_value)
        wallet_view.receive_view.subscribe(wallet_view.receive_view.EVT_SET_LABEL, self.on_set_receive_label)


    def close(self):
        self.account.unsubscribe(self.account.EVT_BALANCE_CHANGED, self.on_balance_changed)
        
    def on_balance_changed(self, event):
        self.wallet_view.balance.set_balance( event.confirmed, event.unconfirmed, event.height)

    def on_new_transaction_item(self, event):
        tx, hash, date, address, name, amount, confirmed = event.item
        self.wallet_view.add_transaction_history_item(hash, date, address.to_base58addr(), name, amount, confirmed)
    
    def on_confirmed_transaction_item(self, event):
        txhash, = event.item
        self.wallet_view.set_confirmed(txhash, True)
    
    def on_new_address_description(self, event):
        self.wallet_view.set_key_description(event.public_key, event.description)
        self.wallet_view.select_key(event.public_key)
        
    def on_send(self, event):
        self.wallet_view.send_view.open()

    
    def on_receive(self, event):
        receive_address = self.account.get_receive_address()
        self.wallet_view.receive_view.set_receive_address(receive_address.to_base58addr())
        self.wallet_view.receive_view.open()
    
    def on_set_receive_label(self, event):
        receive_address = self.wallet_view.receive_view.get_receive_address()
        label = self.wallet_view.receive_view.get_label()
        self.account.set_receive_label(receive_address, label)
        
    @asynch_method  
    def on_select_send_value(self, event): 
        base58addrstr = self.wallet_view.send_view.address()
        amount_str = self.wallet_view.send_view.amount() 
        if not BitcoinAddress.is_valid(base58addrstr, self.account.wallet.runmode):
            self.messages_view.error("Incorrect bitcoin address: %s" % (base58addrstr))
            return
        if not is_float(amount_str):
            self.messages_view.error("Incorrect amount: %s" % (amount_str))
            return
        planned_tx = self.account.create_transaction(int(float(amount_str) * COIN), BitcoinAddress.from_base58addr(base58addrstr), 0)
        self.wallet_view.send_view.close()
        
        passphrases = []
        try:
            if self.account.is_passphrase_required(planned_tx):
                passphrase = yield self.wallet_view.enter_passphrase_view.get_passphrase()
                passphrases.append(passphrase)
            self.account.send_transaction(planned_tx, passphrases)
        except KeyDecryptException as e:
            self.messages_view.error("Unable to decrypt the private keys: please verify the passphrase and try again.")
        except ActionCancelledException:
            pass
        except Exception as e:
            traceback.print_exc()
            self.messages_view.error("Error while sending transaction: %s" % (str(e)))
            
            

    @asynch_method  
    def on_show_hide_private_keys(self, event):
        if self.are_shown_private_keys:
            for public_key, is_crypted, address, description in  self.account.wallet.iterkeys():
                self.wallet_view.set_key_private_key(public_key, "***")
            self.are_shown_private_keys = not self.are_shown_private_keys
        else:
            crypted = False
            for public_key, is_crypted, address, description in  self.account.wallet.iterkeys():
                crypted = crypted or is_crypted
            try:
                if crypted:
                    passphrase = yield self.wallet_view.enter_passphrase_view.get_passphrase()
                    self.account.wallet.unlock([passphrase])
                for public_key, is_crypted, address, description in  self.account.wallet.iterkeys():
                    private_key = self.account.wallet.get_private_key_secret(public_key) 
                    self.wallet_view.set_key_private_key(public_key, hexstr(private_key))
                self.are_shown_private_keys = not self.are_shown_private_keys
            except KeyDecryptException:
                self.messages_view.error("Unable to decrypt the private keys: please verify the passphrase and try again.")
            except ActionCancelledException:
                pass
            except Exception:
                traceback.print_exc()
            finally:
                self.account.wallet.lock()

if __name__ == '__main__':
    #n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo
    import wx
    from coinpy_client.view.wallet.wallet_panel import WalletPanel
    from coinpy.lib.database.bsddb_env import BSDDBEnv
    from coinpy_tests.mock import Mock
    from coinpy.model.protocol.runmode import MAIN, TESTNET
    from coinpy_client.view.message_view import MessageView

    runmode = TESTNET
    wallet_filename= "D:\\repositories\\coinpy\\coinpy-client\\src\\data\\testnet\\wallet_testnet.dat"
    
    directory, filename = os.path.split(wallet_filename)
    
    bsddb_env = BSDDBEnv(directory)
    wallet = Wallet(None, BSDDBWalletDatabase(bsddb_env, filename), runmode)
    balance = Mock({"get_confirmed" : 175877, "get_unconfirmed" : 2828727, "get_height" : 3}, accept_all_methods=True)
    
    wallet_account = Mock(attributes={})
    
    app = wx.App(False)
    frame = wx.Frame(None, size=(600,500))
    wallet_view = WalletPanel(None, frame)
    AccountPresenter(wallet_account, wallet_view, MessageView(None))
    
    frame.Show()
    app.MainLoop()

