from coinpy.model.protocol.messages.types import MSG_BLOCK
from coinpy.model.protocol.messages.message import Message
from coinpy.model.protocol.structures.block import Block

class BlockMessage(Message):
    def __init__(self, block):
        super(BlockMessage,self).__init__(MSG_BLOCK)
        self.block = block
        
    def __str__(self):
        return ("msg_block(%s)" % (str(self.block)))
