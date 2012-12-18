from coinpy.tools.bitcoin.hash160 import hash160
from coinpy.model.address_version import ADDRESSVERSION, ADDRESSVERSIONRUNMODE
from coinpy.tools.bitcoin.base58check import encode_base58check,\
    decode_base58check
from coinpy.model.protocol.runmode import RUNMODE_NAMES
from coinpy.tools.hex import hexstr
from coinpy.lib.vm.script.standard_script_tools import identify_script,\
    tx_pubkeyhash_get_address, tx_pubkey_get_pubkey
from coinpy.model.scripts.standard_scripts import TX_PUBKEYHASH, TX_PUBKEY

class InvalidBitcoinAddress(Exception):
    pass

class BitcoinAddress():
    def __init__(self, hash160, runmode):
        self.hash160 = hash160 # bytestring of length 20
        self.runmode = runmode # MAIN / TESTNET
        
    @staticmethod
    def from_publickey(public_key, runmode):
        return BitcoinAddress(hash160(public_key), runmode)

    @staticmethod
    def from_base58addr(base58addrstr):
        try:
            data = decode_base58check(base58addrstr, 21)
        except Exception as e:
            raise InvalidBitcoinAddress("Unable to decode base58check : %s" % (str(e)))
        if (len(data) != 21):
            raise InvalidBitcoinAddress("BitcoinAddress.from_base58addr(): incorrect length")
        address_version, address = ord(data[0]), data[1:]
        return BitcoinAddress(address, ADDRESSVERSIONRUNMODE[address_version])
    
    def to_base58addr(self):
        return encode_base58check(chr(ADDRESSVERSION[self.runmode]) + self.hash160, preserve_leading_zeros=True)
        
    def to_bytestring(self):
        return chr(ADDRESSVERSION[self.runmode]) + self.hash160

    def to_hexstring(self):
        return hexstr(self.to_bytestring())
        
    @staticmethod
    def from_bytestring(bytestr):
        return BitcoinAddress(bytestr[1:], ADDRESSVERSIONRUNMODE[bytestr[0]])
    
    def get_hash160(self):
        return self.hash160
    
    def __str__(self):
        return "Address(%s,%s)" % (RUNMODE_NAMES[self.runmode], self.to_base58addr())
    
    def __hash__(self):
        return hash(self.hash160)
    
    def __eq__(self, other):
        return (self.runmode == other.runmode) and (self.hash160 == other.hash160)

    @staticmethod
    def is_valid(address_str, runmode):
        try:
            addr = BitcoinAddress.from_base58addr(address_str)
        except InvalidBitcoinAddress:
            return False
        return (addr.runmode == runmode)



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
    print BitcoinAddress(decodehexstr("00600c55b16851c4f9d0e2c82fa161ac8190e04c"), MAIN)
    print BitcoinAddress(decodehexstr("00602005b16851c4f9d0e2c82fa161ac8190e04c"), MAIN)
    print BitcoinAddress.is_valid("112z9tWej11X94khKKzofFgWbdhiXLeHPD", MAIN)    
    print BitcoinAddress.is_valid("1111MJe7b4ZnktoPZabb6DLAKfac8tvx", MAIN)    
    