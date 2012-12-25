from coinpy.model.protocol.messages.types import MSG_GETHEADERS
from coinpy.model.protocol.messages.message import Message

class GetheadersMessage(Message):
    def __init__(self, 
                 blocklocator,
                 hash_stop):
        super(GetheadersMessage, self).__init__(MSG_GETHEADERS)      
        self.blocklocator = blocklocator
        self.hash_stop = hash_stop
        
    def __eq__(self, other):
        return self.blocklocator == other.blocklocator and self.hash_stop == other.hash_stop
    
    def __str__(self):
        return ("getheaders count:%d, start:%s, stop:%s" % (self.start_count, self.hash_start, self.hash_stop))
