from coinpy.tools.hex import hexstr

class WalletKeypair(object):
    def __init__(self, public_key, private_key):
        self.public_key, self.private_key = public_key, private_key
    
    def __str__(self):
        return "WalletKeypair(public:%s private:%s)" % (hexstr(self.public_key), hexstr(self.private_key))