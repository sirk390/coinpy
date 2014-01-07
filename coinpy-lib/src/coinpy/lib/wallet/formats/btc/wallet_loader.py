from coinpy.lib.wallet.formats.btc.file_model import FileHeader, WalletFile,\
    LogIndexChunk, KeysChunk, LogBufferChunk, OutpointsChunk, Metadata,\
    MetadataChunk
from coinpy.lib.wallet.formats.btc.wallet_model import BtcWallet


def new_empty_walletfile():
    return WalletFile( FileHeader(version=1),
                       chunks = [LogIndexChunk( nb_entries=100 ),
                                 LogBufferChunk( size=100*1024 ),
                                 KeysChunk( size=100*1024 ),
                                 OutpointsChunk( size=100*1024 ),
                                 MetadataChunk( Metadata("\0" ** 32, comment="New Wallet"))]
                        )
class WalletFile(object):
    def __init__(self, file_header, log_index_chunk, log_buffer_chunk, keys_chunk, outpoints_chunk, metadata_chunk):
        self.file_header = file_header
        self.log_index_chunk = log_index_chunk
        self.log_buffer_chunk = log_buffer_chunk


def SerilializedWallet(BtcWallet):
    def __init__(self, wallet_file):
        super(SerilializedWallet, self).__init__()
        self.private_keys.ON_CHANGING.subscribe(self.on_changing_privatekeys)
        
    def on_changing_privatekeys():
        pass
"""
class WalletBuilder(object):
    def new_wallet(self, io):
        wallet_file = new_empty_walletfile()
             
        io.write(WalletFileSerializer.serialize(wallet_file))


        wallet = BtcWallet ( )

        wallet.private_keys.ON_CHANGING.subscribe(self.on_changing_privatekeys)
"""