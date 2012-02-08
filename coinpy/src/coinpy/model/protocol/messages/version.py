import time
from coinpy.model.protocol.messages.types import MSG_VERSION
from coinpy.model.protocol.messages.message import message 

class msg_version(message):
    def __init__(self, 
                 version,  #209
                 services, 
                 timestamp, 
                 addr_me, 
                 addr_you, 
                 nonce, 
                 sub_version_num,
                 start_height):
        super(msg_version, self).__init__(MSG_VERSION)
        
        self.version = version
        self.services = services
        self.timestamp = timestamp
        self.addr_me = addr_me
        self.addr_you = addr_you
        self.nonce = nonce
        self.sub_version_num = sub_version_num
        self.start_height = start_height
        
    def __str__(self):
        return ("version:%d services:%d t:%d me:%s you:%s nonce;%d h:%d" % (
                     self.version, 
                     self.services, 
                     self.timestamp,
                     str(self.addr_me),
                     str(self.addr_you),
                     self.nonce,
                     self.start_height)) 

