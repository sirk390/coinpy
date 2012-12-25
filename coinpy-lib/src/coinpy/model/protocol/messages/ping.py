from coinpy.model.protocol.messages.message import Message
from coinpy.model.protocol.messages.types import MSG_PING

class PingMessage(Message):
    def __init__(self):
        super(PingMessage, self).__init__(MSG_PING)       
    
    def __eq__(self, other):
        return True
        
    def __str__(self):
        return ("PingMessage()")
