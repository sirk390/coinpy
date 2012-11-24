
class WalletDatabaseInterface():
    def open(self):
        pass
    
    def get_keypairs(self):
        pass

    def get_wallet_txs(self):
        pass

    def get_names(self):
        pass
    
    def begin_updates(self):
        pass

    def commit_updates(self):
        pass

    def add_name(self, wallet_name):
        pass

    def add_keypair(self, wallet_keypair):
        pass
    
    def get_version(self):
        pass

    def set_version(self, version):
        pass
    
    def get_blocklocator(self):
        pass

    def set_blocklocator(self, blocklocator):
        pass
    