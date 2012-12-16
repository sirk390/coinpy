from coinpy.model.protocol.messages.types import MSG_ADDR
from coinpy.model.protocol.messages.message import Message

class AddrMessage(Message):
    def __init__(self, 
                 timenetaddr_list):
        super(AddrMessage, self).__init__(MSG_ADDR)       
        self.timenetaddr_list = timenetaddr_list
        
    def __eq__(self, other):
        return self.timenetaddr_list == other.timenetaddr_list
    
    def __str__(self):
        return ("addr(%d): %s..." % (len(self.timenetaddr_list), " ".join([str(i) for i in self.timenetaddr_list[0:10]]))) 
