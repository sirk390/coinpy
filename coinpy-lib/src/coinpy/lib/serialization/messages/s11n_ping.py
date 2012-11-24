from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.model.protocol.messages.ping import PingMessage

class PingMessageSerializer(Serializer):
    def serialize(self, ping_message):
        return ("")
    
    def deserialize(self, data, cursor):
        return (PingMessage(), cursor)


    
