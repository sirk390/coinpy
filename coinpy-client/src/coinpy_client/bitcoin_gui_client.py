from coinpy.model.protocol.runmode import MAIN, TESTNET, TESTNET3
import random
from coinpy_client.view.coinpy_gui import CoinpyGUI
from coinpy_client.presenter.coinpy_presenter import CoinpyPresenter
from coinpy_client.bitcoin_client import BitcoinClient
from coinpy_client.model.client_params import ClientParams
from coinpy.node.network.sockaddr import SockAddr
from coinpy_client.config_params import get_config_params

def coinpy_gui_client(client_params):
    view = CoinpyGUI()
    client = BitcoinClient(view.get_logger(), client_params)
    presenter = CoinpyPresenter(client, view)
    presenter.run()

if __name__ == '__main__':
    # testnet faucet: mhFwRrjRNt8hYeWtm9LwqCpCgXjF38RJqn
    # old peer : 88.114.198.141:18333
    mode = 1
    if mode == 1:
        runmode=TESTNET3
        data_directory = r"C:\dev\data\data_testnet_3" 
        seeds=[]
        #seeds = [SockAddr("96.241.176.56", 18333)]
        #seeds = [SockAddr("69.64.46.74", 18333)]
        
        findpeers = True
    if mode == 2:
        runmode=TESTNET
        data_directory = "C:\\dev\\data\\data_testnet" 
        #seeds = [SockAddr("96.241.176.56", 18333)]
        seeds=[]
        findpeers = True
         
        
    params = ClientParams(runmode=runmode, 
                          port=2000, #BITCOIN_PORT[runmode],
                          data_directory=data_directory,
                          findpeers=findpeers,
                          #seeds = [SockAddr("178.79.163.96", 18333)])
                          seeds=seeds) #SockAddr("127.0.0.1", 18333)
    coinpy_gui_client(get_config_params(params))

