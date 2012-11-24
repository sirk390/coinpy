from coinpy.lib.serialization.common.field import Field
from coinpy.lib.serialization.structures.s11n_ipaddrfield import IPAddrSerializer
from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.structures.netaddr import Netaddr


class NetAddrSerializer(Serializer):
    def __init__(self, desc):
        self.NETADDR = Structure([Field("<Q", "services"),
                                  IPAddrSerializer("ip"),
                                  Field(">H", "port")], "netaddr")
        pass

    def serialize(self, a_netaddr):
        data = self.NETADDR.serialize([a_netaddr.services, a_netaddr.ip, a_netaddr.port])
        return (data)

    def deserialize(self, data, cursor):
        (services, ip, port), cursor = self.NETADDR.deserialize(data, cursor)
        return (Netaddr(services, ip, port), cursor)

