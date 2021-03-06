from coinpy.model.protocol.messages.types import MSG_INV
from coinpy.model.protocol.messages.message import Message 

class InvMessage(Message):
    def __init__(self, items):
        super(InvMessage, self).__init__(MSG_INV)
        self.items = items
    
    def __eq__(self, other):
        return self.items == other.items
    
    def __str__(self):
        return ("inv(%d): %s..." % (len(self.items), " ".join([str(i) for i in self.items[0:10]]))) 
