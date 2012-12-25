from coinpy.model.protocol.messages.types import MSG_GETBLOCKS
from coinpy.model.protocol.messages.message import Message

class GetblocksMessage(Message):
    '''
    Example:
        getblocks = GetblocksMessage(
                      BlockLocator([Uint256.from_hexstr("000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")]), 
                      Uint256.zero() )
    '''
    def __init__(self, 
                 block_locator,
                 hash_stop):
        super(GetblocksMessage, self).__init__(MSG_GETBLOCKS)       
        self.block_locator = block_locator
        self.hash_stop = hash_stop
        
    def __eq__(self, other):
        return (self.block_locator == other.block_locator and self.hash_stop == other.hash_stop)
    
    def __str__(self):
        return ("getblocks hash_starts(%d)[%s...], stop:%s" % (len(self.hash_starts), ",".join(str(h) for h in self.hash_starts[:5]), self.hash_stop))


