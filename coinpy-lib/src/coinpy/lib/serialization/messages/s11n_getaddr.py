from coinpy.model.protocol.messages.getaddr import GetaddrMessage
from coinpy.lib.serialization.common.serializer import Serializer

class GetAddrMessageSerializer(Serializer):
    def serialize(self, getaddr):
        return ("")
    
    def deserialize(self, data, cursor):
        return (GetaddrMessage(), cursor)


    
