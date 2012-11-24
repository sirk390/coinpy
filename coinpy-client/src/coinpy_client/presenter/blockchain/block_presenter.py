import wx
from coinpy.lib.bitcoin.hash_block import hash_block
from coinpy.model.protocol.runmode import MAIN
from coinpy.lib.bitcoin.hash_tx import hash_tx
from coinpy.model.constants.bitcoin import COIN
import time
 
#present a BlockSummary() instead of a block
# BlockSummary contains also hash_next and height
class BlockPresenter():
    def __init__(self, block, block_view):
        block_view.set_hash(hash_block(block).get_hexstr())
        block_view.set_previous_block(block.blockheader.hash_prev.get_hexstr())
        
        str_blocktime = time.strftime("%Y-%m-%d %H:%m:%S", time.gmtime(block.blockheader.time))
        block_view.set_time(str_blocktime)
        block_view.set_difficulty("%x" % (block.blockheader.bits))
        
        block_view.set_merkle(block.blockheader.hash_merkle.get_hexstr())
        block_view.set_nonce(str(block.blockheader.nonce))
        for tx in block.transactions:
            amount_out = sum(out.value for out in tx.out_list)
            block_view.add_transaction(hash_tx(tx).get_hexstr(), str(amount_out/ COIN) , "0", "")
            
if __name__ == '__main__':
    from coinpy_client.view.blockchain.block_view import BlockView
    from coinpy.model.genesis import GENESIS

    app = wx.App(False)
    frame = wx.Frame(None, size=(500, 600))
    view = BlockView(frame)
    BlockPresenter(GENESIS[MAIN], view)
    
    frame.Show()
    app.MainLoop()