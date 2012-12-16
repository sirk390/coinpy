from coinpy.model.protocol.messages.types import MSG_ALERT
from coinpy.model.protocol.messages.message import Message
from coinpy.tools.hex import hexstr

class AlertMessage(Message):
    def __init__(self, 
                 payload,
                 signature):
        super(AlertMessage, self).__init__(MSG_ALERT)       
        self.payload = payload
        self.signature = signature
        
    def __eq__(self, other):
        return (self.payload == other.payload and self.signature == other.signature)
    
    def __str__(self):
        return ("AlertMessage(signature:%s,payload:%s)" % (hexstr(self.signature), self.payload)) 


class AlertPayload():
    """Alert Message payload
    
       Attributes:
           version (int) : Alert format version (only 1 is currently defined)
           relay_until  (int) : Timestamp beyond which nodes should stop relaying this alert
           expiration  (int) : Timestamp beyond which this alert is no longer in effect and should be ignored
           id  (int) : Unique ID number for this alert
           cancel  (int) : Alerts with an ID number less than or equal to this number should be canceled: deleted and not accepted in the future 
           set_cancel  (set of int) : alert IDs contained in this set should be canceled as above
           min_ver (int) : Alert applies to versions greater than or equal to this version. Other versions should still relay it.
           max_ver (int) : Alert applies to versions less than or equal to this version. Other versions should still relay it.
           set_sub_ver (set of string) : Nodes that have their subVer contained in this set are affected by the alert.
           priority (int) : Relative priority compared to other alerts
           comment (string) : A comment that is not displayed
           statusbar (string) : Alert message displayed to the user
           reserved (string) : Reserved
        
        Example:
        
            payload = AlertPayload(1, 1329620535, 1329792435, 1010, 1009, set(), 10000, 61000, set(),
                                   100, "", "See bitcoin.org/feb20 if you have trouble connecting after 20 February", "")
    """
    def __init__(self, 
                 version,
                 relay_until,
                 expiration,
                 id,
                 cancel,
                 set_cancel,
                 min_ver,
                 max_ver,
                 set_sub_ver,
                 priority,
                 comment,
                 statusbar,
                 reserved):
        self.version = version
        self.relay_until = relay_until
        self.expiration = expiration
        self.id = id
        self.cancel = cancel
        self.set_cancel = set_cancel
        self.min_ver = min_ver
        self.max_ver = max_ver
        self.set_sub_ver = set_sub_ver
        self.priority = priority
        self.comment = comment
        self.statusbar = statusbar
        self.reserved = reserved

    def __eq__(self, other):
        return (self.version == other.version and 
                self.relay_until == other.relay_until and 
                self.expiration == other.expiration and 
                self.id == other.id and 
                self.cancel == other.cancel and 
                self.set_cancel == other.set_cancel and 
                self.min_ver == other.min_ver and 
                self.max_ver == other.max_ver and 
                self.set_sub_ver == other.set_sub_ver and 
                self.priority == other.priority and 
                self.comment == other.comment and 
                self.statusbar == other.statusbar and 
                self.reserved == other.reserved)
    
    def __str__(self):
        return """"AlertPayload(version:{version},relay_until:{relay_until},expiration:{expiration},id:{id},cancel:{cancel},set_cancel:{set_cancel},min_ver:{min_ver},max_ver:{max_ver},set_sub_ver:{set_sub_ver},priority:{priority},comment:{comment},statusbar:{statusbar},reserved:{reserved})""".format(
                version=self.version,
                relay_until = self.relay_until,
                expiration = self.expiration,
                id = self.id,
                cancel = self.cancel,
                set_cancel = self.set_cancel,
                min_ver = self.min_ver,
                max_ver = self.max_ver,
                set_sub_ver = self.set_sub_ver,
                priority = self.priority,
                comment = self.comment,
                statusbar = self.statusbar,
                reserved = self.reserved)
    
