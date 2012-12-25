from coinpy.model.protocol.messages.types import MSG_VERSION
from coinpy.model.protocol.messages.message import Message 

class VersionMessage(Message):
    """
    Attributes:
      version (int): protocol version number.
      services(SERVICES_NONE=0 or SERVICES_NODE_NETWORK=1): 
      timestamp (int): unix timestamp 
      addr_me (NetAddr)
      addr_you (NetAddr) 
      nonce (int64) 
      sub_version_num (str)
      start_height (int)
    """
    
    def __init__(self, 
                 version,  #209
                 services, 
                 timestamp, 
                 addr_me, 
                 addr_you, 
                 nonce, 
                 sub_version_num,
                 start_height):
        super(VersionMessage, self).__init__(MSG_VERSION)
        
        self.version = version
        self.services = services
        self.timestamp = timestamp
        self.addr_me = addr_me
        self.addr_you = addr_you
        self.nonce = nonce
        self.sub_version_num = sub_version_num
        self.start_height = start_height
    
    def __eq__(self, other):
        return (self.version == other.version and 
                self.services == other.services and 
                self.timestamp == other.timestamp and 
                self.addr_me == other.addr_me and 
                self.addr_you == other.addr_you and 
                self.nonce == other.nonce and 
                self.sub_version_num == other.sub_version_num and 
                self.start_height == other.start_height)
               
    def __str__(self):
        return ("version:%d services:%d t:%d me:%s you:%s nonce;%d h:%d" % (
                     self.version, 
                     self.services, 
                     self.timestamp,
                     str(self.addr_me),
                     str(self.addr_you),
                     self.nonce,
                     self.start_height)) 

