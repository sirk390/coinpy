from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.structures.s11n_invitem import InvitemSerializer
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.model.protocol.messages.inv import InvMessage

class InvMessageSerializer(Serializer):
    INV_ENCODER = VarsizelistSerializer(VarintSerializer(), 
                                        InvitemSerializer())
    
    def serialize(self, inv_msg):
        return (self.INV_ENCODER.serialize(inv_msg.items))
    
    def deserialize(self, data, cursor=0):
        invitems, cursor = self.INV_ENCODER.deserialize(data, cursor)
        return (InvMessage(invitems), cursor)
