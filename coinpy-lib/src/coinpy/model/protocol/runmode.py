
UNITNET, TESTNET, TESTNET3, MAIN  = RUNMODES = range(4)
RUNMODE_NAMES = {UNITNET: "UnitNet", TESTNET : "Testnet", TESTNET3 : "Testnet_3", MAIN : "Main"}

def is_testnet(runmode):
    return (runmode != MAIN)

def is_main(runmode):
    return (runmode == MAIN)
