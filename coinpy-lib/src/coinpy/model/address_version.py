
from coinpy.model.protocol.runmode import MAIN, TESTNET, TESTNET3, UNITNET

ADDRESSVERSION = {MAIN: 0x00, TESTNET: 0x6F, TESTNET3: 0x6F, UNITNET: 0x6F}
ADDRESSVERSIONRUNMODE = dict((versionbyte, runmode) for runmode,  versionbyte in ADDRESSVERSION.iteritems())