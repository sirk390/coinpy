from coinpy.model.protocol.runmode import is_main

PUBKEY_ADDRESS_MAIN = 0
SCRIPT_ADDRESS_MAIN = 5
PUBKEY_ADDRESS_TEST = 111
SCRIPT_ADDRESS_TEST = 196

ADDRESS_TYPES = [PUBKEY_ADDRESS_MAIN, SCRIPT_ADDRESS_MAIN, PUBKEY_ADDRESS_TEST, SCRIPT_ADDRESS_TEST]
ADDRESS_TYPE_NAMES = {PUBKEY_ADDRESS_MAIN : "MAIN/Addr", 
                      SCRIPT_ADDRESS_MAIN : "MAIN/Script", 
                      PUBKEY_ADDRESS_TEST : "TEST/Addr",  
                      SCRIPT_ADDRESS_TEST : "TEST/Script"}

class AddressVersion():
    def __init__(self, value):
        self.value = value
    
    @staticmethod
    def from_byte(value):
        return AddressVersion(value)
    
    def to_byte(self):
        return self.value

    def to_char(self):
        return chr(self.value)

    def is_main(self):
        return (self.value == PUBKEY_ADDRESS_MAIN or self.value ==SCRIPT_ADDRESS_MAIN)

    def is_script_address(self):
        return (self.value == SCRIPT_ADDRESS_MAIN or self.value == SCRIPT_ADDRESS_TEST)
    
    @staticmethod
    def from_parameters(is_main, is_pubkey):
        PARAMS = {(True, True) : SCRIPT_ADDRESS_MAIN,
                  (True, False) : PUBKEY_ADDRESS_MAIN,
                  (False, True) : SCRIPT_ADDRESS_TEST,
                  (False, False) : PUBKEY_ADDRESS_TEST}
        return AddressVersion(PARAMS[(is_main, is_pubkey)])
        
    @staticmethod
    def from_runmode(runmode, is_pubkey=False):
        return AddressVersion.from_parameters(is_main(runmode), is_pubkey)
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __str__(self):
        return ADDRESS_TYPE_NAMES[self.value]
    
    def is_valid_on(self, runmode):
        if is_main(runmode):
            return self.is_main()
        return not self.is_main()

