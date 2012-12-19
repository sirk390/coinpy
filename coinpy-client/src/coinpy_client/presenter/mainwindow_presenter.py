from coinpy_client.presenter.node_presenter import NodePresenter
from coinpy.tools.observer import Observable
from coinpy_client.presenter.pools_presenter import PoolsPresenter
from coinpy_client.presenter.blockchain.blockchain_summary_presenter import BlockchainSummaryPresenter
from coinpy_client.presenter.accountbook_presenter import AccountBookPresenter
import traceback
from coinpy.tools.reactor.asynch import asynch_method
from coinpy_client.view.wallet.enter_passphrase_view import EnterPassphraseView
from coinpy.lib.wallet.bsddb.crypter.passphrase import new_masterkey

class MainWindowPresenter(Observable):
    #    EVT_WALLET_OPENED = Observable.createevent()
    #Shows/hides subwindows (NodeView, WalletBook, Logs)
    def __init__(self, client, mainwindow_view):
        self.mainwindow_view = mainwindow_view
        self.client = client
        self.messages_view = self.mainwindow_view.messages_view
        
        self.node_presenter = NodePresenter(self.client, self.mainwindow_view.node_view)
        self.walletbook_presenter = AccountBookPresenter(self.client, self.client.account_set, self.mainwindow_view.nb_wallet, self.messages_view)
        self.pools_presenter = PoolsPresenter(self.client.node, self.mainwindow_view.pools_view)
        self.blockchain_summary_presenter = BlockchainSummaryPresenter(self.client.blockchain, self.mainwindow_view.blockchain_summary_view)
        self.mainwindow_view.subscribe(self.mainwindow_view.EVT_CMD_OPEN_WALLET, self.on_cmd_open_wallet)
        self.mainwindow_view.subscribe(self.mainwindow_view.EVT_CMD_NEW_WALLET, self.on_cmd_new_wallet)
        self.mainwindow_view.subscribe(self.mainwindow_view.EVT_CMD_CLOSE_WALLET, self.on_cmd_close_wallet)
    
    @asynch_method
    def on_cmd_new_wallet(self, event):
        try:
            passphrase = yield EnterPassphraseView(self.mainwindow_view).get_passphrase()
            self.client.new_wallet(event.file, passphrase)
        except:
            self.mainwindow_view.messages_view.error(str(exc))
        
    def on_cmd_open_wallet(self, event):
        try:
            self.client.open_wallet(event.file)
        except Exception as exc:
            traceback.print_exc()
            self.mainwindow_view.messages_view.error(str(exc))

    def on_cmd_close_wallet(self, event):
        self.client.close_wallet(event.id)
        