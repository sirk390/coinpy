from coinpy_client.bitcoin_gui_client import coinpy_gui_client
from coinpy.model.protocol.runmode import TESTNET
from coinpy_client.model.client_params import ClientParams
from coinpy_client.config_params import get_config_params


def main(params=None):
    coinpy_gui_client(get_config_params(params))
    

if __name__ == '__main__':
    runmode=TESTNET
    data_directory = "data_testnet" if  runmode == TESTNET else "data_main"
    params = ClientParams(runmode=runmode, 
                          data_directory=data_directory)
    main(params)
