from coinpy.lib.serialization.common.serializer import Serializer
from coinpy.lib.serialization.structures.s11n_varstr import VarstrSerializer
from coinpy.lib.serialization.common.structure import Structure
from coinpy.model.protocol.messages.alert import AlertMessage, AlertPayload
from coinpy.lib.serialization.common.varsizelist import VarsizelistSerializer
from coinpy.lib.serialization.structures.s11n_varint import VarintSerializer
from coinpy.lib.serialization.common.field import Field

    
class AlertPayloadSerializer(Serializer):
    PAYLOAD = Structure([Field("<I", "version"),
                         Field("<Q", "relay_until"),
                         Field("<Q", "expiration"),
                         Field("<I", "id"),
                         Field("<I", "cancel"),
                         VarsizelistSerializer(VarintSerializer("count"), VarintSerializer("set_cancel")),
                         Field("<I", "min_ver"),
                         Field("<I", "max_ver"),
                         VarsizelistSerializer(VarintSerializer("count"), VarstrSerializer("set_sub_ver")),
                         Field("<I", "priority"),
                         VarstrSerializer("comment"),
                         VarstrSerializer("statusbar"),
                         VarstrSerializer("reserved")])
    
    def serialize(self, alert_payload):
        return (self.PAYLOAD.serialize([alert_payload.version, 
                                        alert_payload.relay_until,
                                        alert_payload.expiration,
                                        alert_payload.id,
                                        alert_payload.cancel,
                                        alert_payload.set_cancel,
                                        alert_payload.min_ver,
                                        alert_payload.max_ver,
                                        alert_payload.set_sub_ver,
                                        alert_payload.priority,
                                        alert_payload.comment,
                                        alert_payload.statusbar,
                                        alert_payload.reserved]))

    def deserialize(self, data, cursor=0):
        payload_fields, cursor = self.PAYLOAD.deserialize(data, cursor)
        (version, relay_until, expiration, id, cancel, set_cancel, min_ver, max_ver, \
         set_sub_ver, priority,  comment, statusbar, reserved) = payload_fields
        return (AlertPayload(version, relay_until, expiration, id, cancel, 
                             set(set_cancel), min_ver, max_ver, set(set_sub_ver), priority,
                             comment, statusbar, reserved), cursor)


    
class AlertMessageSerializer(Serializer):
    ALERT = Structure([VarstrSerializer("payload"),
                       VarstrSerializer("signature")])
    PAYLOAD = AlertPayloadSerializer()
    def serialize(self, alert_msg):
        payload_data = AlertPayloadSerializer().serialize(alert_msg.payload)
        return (self.ALERT.serialize([payload_data, alert_msg.signature]))

    def deserialize(self, data, cursor=0):
        (payload_data, signature), cursor = self.ALERT.deserialize(data, cursor)
        payload, _ = AlertPayloadSerializer().deserialize(payload_data)
        return (AlertMessage(payload, signature), cursor)


