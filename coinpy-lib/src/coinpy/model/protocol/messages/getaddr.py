from coinpy.model.protocol.messages.types import MSG_GETADDR
from coinpy.model.protocol.messages.message import Message

class GetaddrMessage(Message):
    def __init__(self):
        super(GetaddrMessage, self).__init__(MSG_GETADDR)       

    def __eq__(self, other):
        return True
    
    def __str__(self):
        return ("getaddr")

