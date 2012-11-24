from coinpy.model.protocol.messages.types import MSG_ALERT
from coinpy.model.protocol.messages.message import Message

class AlertMessage(Message):
    def __init__(self, 
                 payload,
                 signature):
        super(AlertMessage, self).__init__(MSG_ALERT)       
        self.payload = payload
        self.signature = signature
        
    def __str__(self):
        return ("AlertMessage(%s): %s" % (self.signature, self.payload)) 
