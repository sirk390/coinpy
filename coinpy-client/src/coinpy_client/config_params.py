from optparse import OptionParser
from coinpy_client.model.client_params import ClientParams
from coinpy.model.protocol.runmode import MAIN, TESTNET
from coinpy.node.network.sockaddr import SockAddr
from coinpy.node.network.bitcoin_port import BITCOIN_PORT
import random
"""
        self.data_directory = data_directory
        self.runmode = runmode
        self.port = port
        self.nonce = nonce
        self.sub_version_num = sub_version_num
        self.targetpeers = targetpeers
        self.logfilename = "coinpy.log"
"""
def command_line_parameters():
    parser = OptionParser()
    parser.add_option("-d", "--data_directory", dest="data_directory", help="location of data directory", metavar="DIR")
    parser.add_option("-m", "--runmode", dest="runmode")
    parser.add_option("-p", "--port", dest="port")
    parser.add_option("-s", "--seeds", dest="seeds")
    parser.add_option("-b", "--no-bootstrap", action="store_true", dest="no_bootstrap")
    parser.add_option("-f", "--no-findpeers", action="store_true", dest="no_findpeers")
    options, args = parser.parse_args()
    params = ClientParams()
    if options.data_directory:
        params.set(data_directory=options.data_directory)
    if options.runmode:
        params.set(runmode={"MAIN" : MAIN, "TESTNET" : TESTNET}[options.runmode])
    if options.port:
        params.set(port=int(options.port))
    if options.seeds:
        params.set(seeds=[SockAddr(ip, int(port)) for ip, port in [addrstr.split(":") for addrstr in options.seeds.split(",")]])
    if options.no_bootstrap:
        params.set(bootstrap=False)
    if options.no_findpeers:
        params.set(findpeers=False)
    return params

def get_config_params(params):
    """Get configuration parameters as ClientParams() object from 
    default_value, configuration file, command_line or function argument
        
    """
    default_args = ClientParams(data_directory="",
                                logfilename="coinpy.log",
                                runmode=MAIN,
                                port=BITCOIN_PORT[MAIN],
                                nonce=random.randint(0, 2**64),
                                sub_version_num="/coinpy:0.0.1/",
                                targetpeers=10,
                                seeds=[])
    client_params = ClientParams()
    client_params.load(default_args)
    if params:
        client_params.load(params)
    client_params.load(command_line_parameters())
    return client_params