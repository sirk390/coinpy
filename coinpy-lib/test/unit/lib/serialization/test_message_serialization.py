import unittest
from coinpy.model.protocol.messages.addr import AddrMessage
from coinpy.model.protocol.structures.netaddr import Netaddr
from coinpy.model.protocol.services import SERVICES_NONE
from coinpy.model.protocol.structures.timenetaddr import Timenetaddr
from coinpy.lib.serialization.messages.s11n_addr import AddrMessageSerializer
from coinpy.tools.hex import hexstr, decodehexstr
from coinpy.model.protocol.messages.alert import AlertMessage, AlertPayload
from coinpy.lib.serialization.messages.s11n_alert import AlertMessageSerializer

class TestMessageSerialization(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_serialize_addr_message(self):
        msg = AddrMessage([Timenetaddr(timestamp=1355658677, netaddr= Netaddr(SERVICES_NONE, "178.3.5.12", 2007)),
                           Timenetaddr(timestamp=1355438677, netaddr= Netaddr(SERVICES_NONE, "32.23.52.122", 23))])
        serialized = AddrMessageSerializer().serialize(msg)
        self.assertEquals(serialized,
                          decodehexstr("02b5b5cd50000000000000000000000000000000000000ffffb203050c07d7555aca50000000000000000000000000000000000000ffff2017347a0017"))
        
    def test_deserialize_addr_message(self):
        serialized = decodehexstr("02b5b5cd50000000000000000000000000000000000000ffffb203050c07d7555aca50000000000000000000000000000000000000ffff2017347a0017")
        msg, _ = AddrMessageSerializer().deserialize(serialized)
        self.assertEquals(msg,
                          AddrMessage([Timenetaddr(timestamp=1355658677, netaddr= Netaddr(SERVICES_NONE, "178.3.5.12", 2007)),
                                       Timenetaddr(timestamp=1355438677, netaddr= Netaddr(SERVICES_NONE, "32.23.52.122", 23))]))

    def test_serialize_alert_message(self):
        alert_msg = AlertMessage(AlertPayload(1, 1329620535, 1329792435, 1010, 1009, set(), 10000, 61000, set(),
                                   100, "", "See bitcoin.org/feb20 if you have trouble connecting after 20 February", "")
                                 , decodehexstr("30450221008389df45f0703f39ec8c1cc42c13810ffcae14995bb648340219e353b63b53eb022009ec65e1c1aaeec1fd334c6b684bde2b3f573060d5b70c3a46723326e4e8a4f1"))
        serialized_msg = AlertMessageSerializer().serialize(alert_msg)
        self.assertEquals(serialized_msg,
                          decodehexstr("73010000003766404f00000000b305434f00000000f2030000f1030000001027000048ee00000064000000004653656520626974636f696e2e6f72672f666562323020696620796f7520686176652074726f75626c6520636f6e6e656374696e67206166746572203230204665627275617279004730450221008389df45f0703f39ec8c1cc42c13810ffcae14995bb648340219e353b63b53eb022009ec65e1c1aaeec1fd334c6b684bde2b3f573060d5b70c3a46723326e4e8a4f1"))

    def test_deserialize_alert_message(self):
        serialized_alert = decodehexstr("73010000003766404f00000000b305434f00000000f2030000f1030000001027000048ee00000064000000004653656520626974636f696e2e6f72672f666562323020696620796f7520686176652074726f75626c6520636f6e6e656374696e67206166746572203230204665627275617279004730450221008389df45f0703f39ec8c1cc42c13810ffcae14995bb648340219e353b63b53eb022009ec65e1c1aaeec1fd334c6b684bde2b3f573060d5b70c3a46723326e4e8a4f1")
        
        alert_msg, _ = AlertMessageSerializer().deserialize(serialized_alert)
        expected_msg = AlertMessage(AlertPayload(1, 1329620535, 1329792435, 1010, 1009, set(), 10000, 61000, set(),
                                 100, "", "See bitcoin.org/feb20 if you have trouble connecting after 20 February", "")
                                 , decodehexstr("30450221008389df45f0703f39ec8c1cc42c13810ffcae14995bb648340219e353b63b53eb022009ec65e1c1aaeec1fd334c6b684bde2b3f573060d5b70c3a46723326e4e8a4f1"))
        self.assertEquals(alert_msg, expected_msg)
    
    
        
if __name__ == '__main__':
    unittest.main()
    
