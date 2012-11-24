from coinpy.model.protocol.runmode import MAIN, TESTNET
import random
from coinpy_client.bitcoin_client import BitcoinClient
import log
from coinpy.tools.reactor.reactor import Reactor
from coinpy_client.model.client_params import ClientParams

def main(runmode=TESTNET):
    data_directory = "data_testnet" if  runmode == TESTNET else "data_main"
    params = ClientParams(data_directory,
                          runmode=runmode,
                          port=8080,
                          nonce=random.randint(0, 2**64),
                          sub_version_num="/coinpy:0.0.1/",
                          targetpeers=5)
    reactor = Reactor()
    client = BitcoinClient(reactor, log.createlogger(), params)
    client.start()
  
if __name__ == '__main__':
    main(runmode=TESTNET)
    