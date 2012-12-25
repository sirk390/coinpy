from coinpy.model.protocol.messages.verack import VerackMessage
from coinpy.lib.serialization.common.serializer import Serializer

class VerackMessageSerializer(Serializer):
    def serialize(self, verack):
        return ("")
    
    def deserialize(self, data, cursor=0):
        return (VerackMessage(), cursor)


    
