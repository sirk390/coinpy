from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.model.protocol.messages.getdata import GetdataMessage
from coinpy.lib.serialization.structures.s11n_invitem import InvitemSerializer
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer

class GetdataMessageSerializer(Serializer):
    GETDATA_ENC = VarsizelistSerializer(VarintSerializer(), 
                                        InvitemSerializer())
    
    def serialize(self, getdata_msg):
        return (self.GETDATA_ENC.serialize(getdata_msg.invitems))

    def deserialize(self, data, cursor=0):
        invitems, cursor = self.GETDATA_ENC.deserialize(data, cursor)
        return (GetdataMessage(invitems), cursor)

    
