from coinpy.tools.bitcoin.hash160 import hash160
from coinpy.model.address_version import AddressVersion, PUBKEY_ADDRESS_MAIN
from coinpy.tools.bitcoin.base58check import encode_base58check,\
    decode_base58check
from coinpy.tools.hex import hexstr
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY
from coinpy.lib.vm.script.identify_scripts import identify_script
from coinpy.lib.vm.script.standard_scripts import tx_pubkeyhash_get_address,\
    tx_pubkey_get_pubkey
from coinpy.model.protocol.runmode import RUNMODE_NAMES

class InvalidBitcoinAddress(Exception):
    pass

class BitcoinAddress():
    """
       hash160 (bytestring of length 20)
       address_version (instance of AddressVersion)
    """
    def __init__(self, hash160, address_version):
        self.hash160 = hash160 # 
        self.address_version = address_version

    @staticmethod
    def from_publickey(public_key, runmode):
        return BitcoinAddress(hash160(public_key), AddressVersion.from_runmode(runmode))

    @staticmethod
    def from_bytestring(bytestr):
        if (len(bytestr) != 21):
            raise InvalidBitcoinAddress("BitcoinAddress.from_base58addr(): incorrect length")
        return BitcoinAddress(hash160=bytestr[1:], address_version=AddressVersion.from_byte(ord(bytestr[0])))

    @staticmethod
    def from_base58addr(base58addrstr):
        try:
            bytestr = decode_base58check(base58addrstr, True)
        except Exception as e:
            raise InvalidBitcoinAddress("Unable to decode base58check : %s" % (str(e)))
        if len(bytestr) != 21:
            raise InvalidBitcoinAddress("Invalid length : %d" % (len(bytestr)))
        return BitcoinAddress.from_bytestring(bytestr)

    def to_base58addr(self):
        return encode_base58check(self.address_version.to_char() + self.hash160, preserve_leading_zeros=True)
        
    def to_bytestring(self):
        return self.address_version.to_char() + self.hash160

    def to_hexstring(self):
        return hexstr(self.to_bytestring())
        
    def get_hash160(self):
        return self.hash160

    def get_addr_version(self):
        return self.address_version
  
    def is_valid_on(self, runmode=None):
        return self.address_version.is_valid_on(runmode)
    
    @staticmethod
    def is_valid(address_str, runmode=None):
        try:
            addr = BitcoinAddress.from_base58addr(address_str)
        except InvalidBitcoinAddress:
            return False
        return addr.is_valid_on(runmode)

    def __str__(self):
        return "Address(%s,%s)" % (str(self.address_version), self.to_base58addr())
    
    def __hash__(self):
        return hash((self.address_version, self.hash160))
    
    def __eq__(self, other):
        return (self.address_version == other.address_version) and (self.hash160 == other.hash160)


def extract_txout_address(txout, runmode):
    script_type = identify_script(txout.script)
    # if unknown script type, return None
    if (script_type is None): 
        return None 
    if script_type == TX_PUBKEYHASH:
        return BitcoinAddress(tx_pubkeyhash_get_address(txout.script), runmode)
    if script_type == TX_PUBKEY:
        return BitcoinAddress.from_publickey(tx_pubkey_get_pubkey(txout.script), runmode)
    return None 

def extract_txout_bytestr_address(txout):
    script_type = identify_script(txout.script)
    # if unknown script type, return None
    if (script_type is None): 
        raise Exception("Unknown script type")
    if script_type == TX_PUBKEYHASH:
        return tx_pubkeyhash_get_address(txout.script)
    if script_type == TX_PUBKEY:
        return hash160(tx_pubkey_get_pubkey(txout.script))
    raise Exception("Unexpected script type")

    
if __name__ == '__main__':
    from coinpy.model.protocol.runmode import TESTNET, MAIN
    from coinpy.tools.hex import decodehexstr
    assert BitcoinAddress.is_valid("n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo", TESTNET)
    assert not BitcoinAddress.is_valid("n4NsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo", TESTNET)
    print BitcoinAddress.is_valid("1H5azJoKoYd92DxjXX7k7gejpbLVMAczAi", MAIN)    
    print BitcoinAddress.is_valid("1H1hQVMZ6bpyGNWboJQT4aouDSksBnZWL3", MAIN)
    print BitcoinAddress.from_base58addr("n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo")
    print BitcoinAddress.from_base58addr("1H5azJoKoYd92DxjXX7k7gejpbLVMAczAi")
    print BitcoinAddress.from_base58addr("1H5azJoKoYd92DxjXX7k7gejpbLVMAczAi").to_base58addr()
    print BitcoinAddress.from_base58addr("1H5azJoKoYd92DxjXX7k7gejpbLVMAczAi").to_hexstring()
    print BitcoinAddress.from_base58addr("n4MsBRWD7VxKGsqYRSLaFZC6hQrsrKLaZo").to_base58addr()
    print BitcoinAddress(decodehexstr("00600c55b16851c4f9d0e2c82fa161ac8190e04c"), AddressVersion(PUBKEY_ADDRESS_MAIN))
    print BitcoinAddress(decodehexstr("00602005b16851c4f9d0e2c82fa161ac8190e04c"), AddressVersion(PUBKEY_ADDRESS_MAIN))
    print BitcoinAddress.is_valid("112z9tWej11X94khKKzofFgWbdhiXLeHPD", MAIN)    
    print BitcoinAddress.is_valid("1111MJe7b4ZnktoPZabb6DLAKfac8tvx", MAIN)    
    