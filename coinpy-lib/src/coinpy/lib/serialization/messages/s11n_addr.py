from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.lib.serialization.structures.s11n_timenetaddr import TimenetaddrSerializer
from coinpy.model.protocol.messages.addr import AddrMessage

class AddrMessageSerializer(Serializer):
    ADDR = VarsizelistSerializer(VarintSerializer("count"),
                                 TimenetaddrSerializer())
    
    def serialize(self, addr_msg):
        return (self.ADDR.serialize(addr_msg.addr_list))

    def deserialize(self, data, cursor):
        addr_list, cursor = self.ADDR.deserialize(data, cursor)
        return (AddrMessage(addr_list), cursor)


    
