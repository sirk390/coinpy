import unittest
from coinpy.model.protocol.messages.addr import AddrMessage
from coinpy.model.protocol.structures.netaddr import Netaddr
from coinpy.model.protocol.services import SERVICES_NONE, SERVICES_NODE_NETWORK
from coinpy.model.protocol.structures.timenetaddr import Timenetaddr
from coinpy.lib.serialization.messages.s11n_addr import AddrMessageSerializer
from coinpy.tools.hex import hexstr, decodehexstr
from coinpy.model.protocol.messages.alert import AlertMessage, AlertPayload
from coinpy.lib.serialization.messages.s11n_alert import AlertMessageSerializer
from coinpy.model.protocol.structures.block import Block
from coinpy.model.protocol.structures.blockheader import BlockHeader
from coinpy.model.protocol.structures.uint256 import Uint256
from coinpy.model.protocol.structures.outpoint import Outpoint
from coinpy.model.protocol.structures.tx_in import TxIn
from coinpy.model.scripts.instruction import Instruction
from coinpy.model.scripts.script import Script
from coinpy.model.protocol.structures.tx_out import TxOut
from coinpy.model.protocol.structures.tx import Tx
from coinpy.model.scripts.opcodes import OP_CHECKSIG, OP_DUP, OP_EQUALVERIFY,\
    OP_HASH160, OP_EQUAL
from coinpy.model.protocol.messages.block import BlockMessage
from coinpy.lib.serialization.messages.s11n_block import BlockMessageSerializer
from coinpy.model.protocol.messages.getaddr import GetaddrMessage
from coinpy.lib.serialization.messages.s11n_getaddr import GetaddrMessageSerializer
from coinpy.model.protocol.messages.getblocks import GetblocksMessage
from coinpy.model.protocol.structures.blocklocator import BlockLocator
from coinpy.lib.serialization.messages.s11n_getblocks import GetblocksMessageSerializer
from coinpy.model.protocol.messages.getdata import GetdataMessage
from coinpy.model.protocol.structures.invitem import Invitem, INV_TX, INV_BLOCK
from coinpy.lib.serialization.messages.s11n_getdata import GetdataMessageSerializer
from coinpy.model.protocol.messages.getheaders import GetheadersMessage
from coinpy.lib.serialization.messages.s11n_getheaders import GetheadersMessageSerializer
from coinpy.model.protocol.messages.inv import InvMessage
from coinpy.lib.serialization.messages.s11n_inv import InvMessageSerializer
from coinpy.model.protocol.messages.ping import PingMessage
from coinpy.lib.serialization.messages.s11n_ping import PingMessageSerializer
from coinpy.model.protocol.messages.tx import TxMessage
from coinpy.lib.serialization.messages.s11n_tx import TxMessageSerializer
from coinpy.model.protocol.messages.verack import VerackMessage
from coinpy.lib.serialization.messages.s11n_verack import VerackMessageSerializer
from coinpy.model.protocol.messages.version import VersionMessage
from coinpy.lib.serialization.messages.s11n_version import VersionMessageSerializer

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
    
    def test_serialize_block_message(self):
        #block 381 on testnet 3 (first block with exactly 2 transactions)
        block_msg = BlockMessage(
                            Block(blockheader=BlockHeader(version=1, 
                                  hash_prev=Uint256.from_hexstr("00000000d2a17cbe6e38439f60111911c2cca0a551ccfac41a7efa659048b9c5"), 
                                  hash_merkle=Uint256.from_hexstr("83c4a9e0d7b0bc6be667bf916e3d3dea5949c235e3db841d44a8a222bb3bdba0"), 
                                  time=1296728938,
                                  bits=486604799,
                                  nonce=1712527364), 
                            transactions=[
                    Tx(version=1, 
                        in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"),index=4294967295), 
                           script=Script(instructions=[Instruction(4,  decodehexstr("6a834a4d")),Instruction(1,  decodehexstr("7e")),Instruction(6,  decodehexstr("2f503253482f"))]), 
                           sequence=4294967295)], 
                        out_list=[TxOut(value=5000000000, 
                            script=Script(instructions=[Instruction(33,  decodehexstr("03dac3fb8de40965f42fb4afb3baa07d3304bc2aa28cfc25f12b52f1523681451d")),Instruction(OP_CHECKSIG)]))], 
                        locktime=0),
                    Tx(version=1, 
                        in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("6749762ae220c10705556799dcec9bb6a54a7b881eb4b961323a3363b00db518"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("3046022100e49de3c89180769db346145cdda48323ddecc2af0041293432528767b18407650221009f7878deb054e4f9c0e6aecbe6de15f5d829041c11f7952d33e96c76ada1258b01"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("c04c413576307737f3ad48efe5d509ebc883e1d04822b3a2eccf6a80a4482932"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("3046022100ba88d34e4d4fd85ab5e4d77cb74f71c87a24235bcbe39cf4334633f70ff27233022100b5aa1b96bab59457d3d837473de1e4f9f89ba3ee39964463952271c5b4140fa001"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("72d4fc43ac576a4b2f1f35e1b310a2d83a1012a36fdc7813ec237646950233cf"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("3046022100b21560dfda52352c4416c1e48496659ea3d29e4e25706a991986864210bc759e0221009c1e45af6e2eba0883a862442d85a2b48c3395e35a4276f535cd70d45a971c7401"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("2d34482568c53b9831ef765280f59fd151c3f8ec09f88867f6b85d974d0fedee"),index=0), 
                           script=Script(instructions=[Instruction(72,  decodehexstr("3045022100e02cc0b4bf8a126807b1577819944c1bb13e8f4028cf7df0a0729013d511b071022010a1bcdefca334588939f9fe40e0d8607588191684fce0f46180a139305b8b4001"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("a5dd9470792c9ad6fda110d4b19c9f2b2b07eb96d239530a0e1ec0b12f0aacc8"),index=0), 
                           script=Script(instructions=[Instruction(72,  decodehexstr("3045022016ba8f50d7f30be7e4a68c3d50368d577e2ef6c8b60842725ae636b2985776fc022100bb39d47d1955ffca47920d743bcd6f05b31ea2bf3dc7ede225eb4c901126b48901"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("1b24cec4ce0519df028af441934f161c3fdbc6bbf611d33ff39e0b68f03cb0f1"),index=0), 
                           script=Script(instructions=[Instruction(72,  decodehexstr("304502201dbbfabc47f6da84ceedbc92b792d4a8ef632f0bddf7ebfad5ca21f3731f450502210098751ccf37fd97ff82446486d4c1d62860c2080a1128ea5ddb0d30bfde3cd7a801"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("ed97bd0230c4fc9e53e6acd280a873db5639a087ff5874fe80a674c08a89e61f"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("3046022100f8a83fadb06af9c0cc730f17ae47fe7a09cada9eae623b8dd86bf365ef0e20480221009a10b073b2a8b313d975f801213efdf12b94141d7b6a8e98de3b0c67ee1cef4c01"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("a45f9a24d946feda1b6c2e571ba941ac09155f4d6a59733586e9cf13025cd86f"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("3046022100f3e98f3e76cc0f533b0e1cccd82650b704e31e3e7e62bf81bb474cf2add58ebf022100f77003eec814a3336cc305b8461cf3ccb19b1f18f06f66208ed31c3e468466ed01"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("dd6e072eb7e092acac3826c1d346218c188d70789504fc16795e51a656a0939e"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("30460221008ee8d7348aed82a8d074753ab4c8dbdd28a668da821269c4cd0c5c253738cab7022100b06a0208d60af1be6303dd883fd05f964a42f7de317761641ec1158944f52b6b01"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("d3d98f948569afdd86421523a954854773346ebb36d8747d375dcdd8737bcc0e"),index=0), 
                           script=Script(instructions=[Instruction(72,  decodehexstr("30450221008159ed783bc717ff5a6502cd87a8d8144fae74c6fc6943a5a38da7170203cb3802207e31577a576bc01510cb2280f918a371f63eee44cd2b4490c0994d261787916e01"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("5cc0a6a52aa841918915d039f0045a321afba69f241824ab52442d0a9f6e9678"),index=0), 
                           script=Script(instructions=[Instruction(71,  decodehexstr("304402206655b13198e413ac8f1aa8926d4617560758cf8b5045afdfc9116da0873ed89802205db55cf3f398467bfc6997f68c881e5f2a7225293ebbd2af40d15df6de4ef87701"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("7c2703dfb6b2c74d07c3f54a7f1b6484d07d7d7f30fbe2fe1570debe6b09f269"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("3046022100c9199296673a1beae598a6d2348ef13ad1b9f15eebaa825d2282adf017cbb5f0022100b54934e40ff0194a53dcaa9d017c36a93dbb53aa45fe21ab93b07fbb58570d5501"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("3083cb9808088da30888073f5ac952c3a02ba54239736bc32ed63fd446b1113c"),index=0), 
                           script=Script(instructions=[Instruction(71,  decodehexstr("3044022004c64773b9e6a17cfca7ff583be650104c0538940289b2da8f8bebbd32e486b302200174d8f0938a0f9eeab4c4b137581e032f06d4740e3b0ad9d0423a0a8de65af101"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("763c1bef6943e02d9c0696ebe183922e26575c489def07a9b989faad373cac59"),index=0), 
                           script=Script(instructions=[Instruction(72,  decodehexstr("30450220306f3ac72de9dbeb1ec139e4e89cc3b3b9bcb63747bf0e165fcfc773f3669832022100c00a16800f16bf1c71ac6c2989b42d974b0ec2f3e3671325fb2cae52a1c569d801"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("b77bfe8240e197a3c004e3144613ab29cc5cbd6df382abe586d98d81eeecbbb4"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("3046022100ed68e0303052b41ffd80c1e905cee5547e92422d43b73e473a615e4a47146bb5022100ecab3f92c62477350753b4efea19d608fcce15b1b2c38fbe905e9d1f9ad7631f01"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("8404eec9135a198ff37ff2f3b605f34deb68b354c1e8a60d98c8e19aacbb4675"),index=0), 
                           script=Script(instructions=[Instruction(72,  decodehexstr("304502202288566af2b68b6982d1244e293ea3d7c156a425329b7f61b272e4deec317bea022100d9739976b442d35c32830cb2c105e0d7275f7efaa99eaeea4b24a553267a31fc01"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("77b6bab82fa6183f1a83b70551e22b7a55240b479f0872af9d34bae5d15458d1"),index=0), 
                           script=Script(instructions=[Instruction(72,  decodehexstr("304502206e3a23075e0248ea8cabc7c875b4cfd9f036c1c4f358a00ec152fc96d1cb6cf8022100d34c018815f63c65f5364061369382b31d579cd6d8a4afe9ec1f03ba66d7717801"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("7e9ece75efbb59dfb38e4245fa19474336636db25385606adec1c2317f6a68df"),index=0), 
                           script=Script(instructions=[Instruction(72,  decodehexstr("304502200a22a24a8f817a2f24d3f8c2670f3cb25cd389ce25e0d45eeb0aea08563c5c9802210081ff14edb230a44e5b52e35f573676096a937fc27cc830b153b229b92cac75c101"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("27b2f3eafa9e5696eb76a8960c95502e727b640f344d031aa3c5991ba9fe26d2"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("30460221009684e60a7fd61362d0dad79858044aa4a7b878b3f0bd432e384fe4c7e6c90bde0221009883e4f739cffe574bac5bed0a4e69708433973a2490d9415d303614fc31be4701"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("718f8928d46e07dfad7ce17e4747ef23536f83699859480002dc38a40ec640f6"),index=0), 
                           script=Script(instructions=[Instruction(72,  decodehexstr("30450220028eb7617dc161a282512c81975d41a1594c05f34cb26fb759682bf784da7071022100a0913abea7229b3c465a4fa32dc861f72ef684e8dd3f19aac5f0f74ea39c03cf01"))]), 
                           sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("cc61baf9815306f8da8f9de105023fde0ddc49269d8ac67a6f3c88b1492a9dd5"),index=0), 
                           script=Script(instructions=[Instruction(73,  decodehexstr("30460221009f5b27dfd397423a04cab52ee6e8215e290e9666309f0f59f5bc5f6c207d3639022100f5a79133db2cc786140aeee0bf7c8a81adca6071928e8210f1c9f0c653e2f04201"))]), 
                           sequence=4294967295)], 
                        out_list=[TxOut(value=4989000000, 
                            script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("944a7d4b3a8d3a5ecf19dfdfd8dcc18c6f1487dd")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])),TxOut(value=100011000000, 
                            script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("32040178c5cf81cb200ab99af1131f187745b515")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)]))], 
                        locktime=0)]))
        serialized_msg = BlockMessageSerializer().serialize(block_msg)
        self.assertEquals(hexstr(serialized_msg),
                          "01000000c5b9489065fa7e1ac4facc51a5a0ccc2111911609f43386ebe7ca1d200000000a0db3bbb22a2a8441d84dbe335c24959ea3d3d6e91bf67e66bbcb0d7e0a9c4836a834a4dffff001d041813660201000000010000000000000000000000000000000000000000000000000000000000000000ffffffff0e046a834a4d017e062f503253482fffffffff0100f2052a01000000232103dac3fb8de40965f42fb4afb3baa07d3304bc2aa28cfc25f12b52f1523681451dac00000000010000001518b50db063333a3261b9b41e887b4aa5b69becdc9967550507c120e22a764967000000004a493046022100e49de3c89180769db346145cdda48323ddecc2af0041293432528767b18407650221009f7878deb054e4f9c0e6aecbe6de15f5d829041c11f7952d33e96c76ada1258b01ffffffff322948a4806acfeca2b32248d0e183c8eb09d5e5ef48adf33777307635414cc0000000004a493046022100ba88d34e4d4fd85ab5e4d77cb74f71c87a24235bcbe39cf4334633f70ff27233022100b5aa1b96bab59457d3d837473de1e4f9f89ba3ee39964463952271c5b4140fa001ffffffffcf330295467623ec1378dc6fa312103ad8a210b3e1351f2f4b6a57ac43fcd472000000004a493046022100b21560dfda52352c4416c1e48496659ea3d29e4e25706a991986864210bc759e0221009c1e45af6e2eba0883a862442d85a2b48c3395e35a4276f535cd70d45a971c7401ffffffffeeed0f4d975db8f66788f809ecf8c351d19ff5805276ef31983bc5682548342d0000000049483045022100e02cc0b4bf8a126807b1577819944c1bb13e8f4028cf7df0a0729013d511b071022010a1bcdefca334588939f9fe40e0d8607588191684fce0f46180a139305b8b4001ffffffffc8ac0a2fb1c01e0e0a5339d296eb072b2b9f9cb1d410a1fdd69a2c797094dda50000000049483045022016ba8f50d7f30be7e4a68c3d50368d577e2ef6c8b60842725ae636b2985776fc022100bb39d47d1955ffca47920d743bcd6f05b31ea2bf3dc7ede225eb4c901126b48901fffffffff1b03cf0680b9ef33fd311f6bbc6db3f1c164f9341f48a02df1905cec4ce241b000000004948304502201dbbfabc47f6da84ceedbc92b792d4a8ef632f0bddf7ebfad5ca21f3731f450502210098751ccf37fd97ff82446486d4c1d62860c2080a1128ea5ddb0d30bfde3cd7a801ffffffff1fe6898ac074a680fe7458ff87a03956db73a880d2ace6539efcc43002bd97ed000000004a493046022100f8a83fadb06af9c0cc730f17ae47fe7a09cada9eae623b8dd86bf365ef0e20480221009a10b073b2a8b313d975f801213efdf12b94141d7b6a8e98de3b0c67ee1cef4c01ffffffff6fd85c0213cfe9863573596a4d5f1509ac41a91b572e6c1bdafe46d9249a5fa4000000004a493046022100f3e98f3e76cc0f533b0e1cccd82650b704e31e3e7e62bf81bb474cf2add58ebf022100f77003eec814a3336cc305b8461cf3ccb19b1f18f06f66208ed31c3e468466ed01ffffffff9e93a056a6515e7916fc049578708d188c2146d3c12638acac92e0b72e076edd000000004a4930460221008ee8d7348aed82a8d074753ab4c8dbdd28a668da821269c4cd0c5c253738cab7022100b06a0208d60af1be6303dd883fd05f964a42f7de317761641ec1158944f52b6b01ffffffff0ecc7b73d8cd5d377d74d836bb6e3473478554a923154286ddaf6985948fd9d300000000494830450221008159ed783bc717ff5a6502cd87a8d8144fae74c6fc6943a5a38da7170203cb3802207e31577a576bc01510cb2280f918a371f63eee44cd2b4490c0994d261787916e01ffffffff78966e9f0a2d4452ab2418249fa6fb1a325a04f039d015899141a82aa5a6c05c000000004847304402206655b13198e413ac8f1aa8926d4617560758cf8b5045afdfc9116da0873ed89802205db55cf3f398467bfc6997f68c881e5f2a7225293ebbd2af40d15df6de4ef87701ffffffff69f2096bbede7015fee2fb307f7d7dd084641b7f4af5c3074dc7b2b6df03277c000000004a493046022100c9199296673a1beae598a6d2348ef13ad1b9f15eebaa825d2282adf017cbb5f0022100b54934e40ff0194a53dcaa9d017c36a93dbb53aa45fe21ab93b07fbb58570d5501ffffffff3c11b146d43fd62ec36b733942a52ba0c352c95a3f078808a38d080898cb83300000000048473044022004c64773b9e6a17cfca7ff583be650104c0538940289b2da8f8bebbd32e486b302200174d8f0938a0f9eeab4c4b137581e032f06d4740e3b0ad9d0423a0a8de65af101ffffffff59ac3c37adfa89b9a907ef9d485c57262e9283e1eb96069c2de04369ef1b3c7600000000494830450220306f3ac72de9dbeb1ec139e4e89cc3b3b9bcb63747bf0e165fcfc773f3669832022100c00a16800f16bf1c71ac6c2989b42d974b0ec2f3e3671325fb2cae52a1c569d801ffffffffb4bbecee818dd986e5ab82f36dbd5ccc29ab134614e304c0a397e14082fe7bb7000000004a493046022100ed68e0303052b41ffd80c1e905cee5547e92422d43b73e473a615e4a47146bb5022100ecab3f92c62477350753b4efea19d608fcce15b1b2c38fbe905e9d1f9ad7631f01ffffffff7546bbac9ae1c8980da6e8c154b368eb4df305b6f3f27ff38f195a13c9ee0484000000004948304502202288566af2b68b6982d1244e293ea3d7c156a425329b7f61b272e4deec317bea022100d9739976b442d35c32830cb2c105e0d7275f7efaa99eaeea4b24a553267a31fc01ffffffffd15854d1e5ba349daf72089f470b24557a2be25105b7831a3f18a62fb8bab677000000004948304502206e3a23075e0248ea8cabc7c875b4cfd9f036c1c4f358a00ec152fc96d1cb6cf8022100d34c018815f63c65f5364061369382b31d579cd6d8a4afe9ec1f03ba66d7717801ffffffffdf686a7f31c2c1de6a608553b26d6336434719fa45428eb3df59bbef75ce9e7e000000004948304502200a22a24a8f817a2f24d3f8c2670f3cb25cd389ce25e0d45eeb0aea08563c5c9802210081ff14edb230a44e5b52e35f573676096a937fc27cc830b153b229b92cac75c101ffffffffd226fea91b99c5a31a034d340f647b722e50950c96a876eb96569efaeaf3b227000000004a4930460221009684e60a7fd61362d0dad79858044aa4a7b878b3f0bd432e384fe4c7e6c90bde0221009883e4f739cffe574bac5bed0a4e69708433973a2490d9415d303614fc31be4701fffffffff640c60ea438dc020048599869836f5323ef47477ee17caddf076ed428898f7100000000494830450220028eb7617dc161a282512c81975d41a1594c05f34cb26fb759682bf784da7071022100a0913abea7229b3c465a4fa32dc861f72ef684e8dd3f19aac5f0f74ea39c03cf01ffffffffd59d2a49b1883c6f7ac68a9d2649dc0dde3f0205e19d8fdaf8065381f9ba61cc000000004a4930460221009f5b27dfd397423a04cab52ee6e8215e290e9666309f0f59f5bc5f6c207d3639022100f5a79133db2cc786140aeee0bf7c8a81adca6071928e8210f1c9f0c653e2f04201ffffffff0240195e29010000001976a914944a7d4b3a8d3a5ecf19dfdfd8dcc18c6f1487dd88acc0c01e49170000001976a91432040178c5cf81cb200ab99af1131f187745b51588ac00000000")
            
    def test_deserialize_block_message(self):
        #block 22 on testnet 3
        serialized_block_msg= decodehexstr("0100000073379e3ff3dffd006e0090e52ac571a9a309490a23e64d15f8af291a0000000051f1c5b2b7c8f980e7715b4d3ce0180f99c44a16fc9c00ede2f5984b8d7cc22d16ed494dffff001d0082467f0101000000010000000000000000000000000000000000000000000000000000000000000000ffffffff0f0416ed494d02fa00062f503253482fffffffff0100f2052a01000000232103b787920594cb47fbfccee915befae40ac2e2b295224460eee075ad0ada4c0c54ac00000000")
        
        block_msg, _ = BlockMessageSerializer().deserialize(serialized_block_msg)
        expected_block_msg = BlockMessage(Block(blockheader=BlockHeader(version=1, 
                          hash_prev=Uint256.from_hexstr("000000001a29aff8154de6230a4909a3a971c52ae590006e00fddff33f9e3773"), 
                          hash_merkle=Uint256.from_hexstr("2dc27c8d4b98f5e2ed009cfc164ac4990f18e03c4d5b71e780f9c8b7b2c5f151"), 
                          time=1296690454,
                          bits=486604799,
                          nonce=2135327232), 
                    transactions=[Tx(version=1, 
                        in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("0000000000000000000000000000000000000000000000000000000000000000"),index=4294967295), 
                           script=Script(instructions=[Instruction(4,  decodehexstr("16ed494d")),Instruction(2,  decodehexstr("fa00")),Instruction(6,  decodehexstr("2f503253482f"))]), 
                           sequence=4294967295)], 
                        out_list=[TxOut(value=5000000000, 
                            script=Script(instructions=[Instruction(33,  decodehexstr("03b787920594cb47fbfccee915befae40ac2e2b295224460eee075ad0ada4c0c54")),Instruction(OP_CHECKSIG)]))], 
                        locktime=0)]))
        self.assertEquals(block_msg, expected_block_msg)
    
    def test_serialize_getaddr_message(self):
        getaddr_msg = GetaddrMessage()
        serialized_msg = GetaddrMessageSerializer().serialize(getaddr_msg)
        self.assertEquals(hexstr(serialized_msg), "")

    def test_deserialize_getaddr_message(self):
        getaddr_msg, _ = GetaddrMessageSerializer().deserialize("")
        self.assertEquals(getaddr_msg,GetaddrMessage())

    def test_serialize_getblocks_message(self):
        getblocks_msg = GetblocksMessage(BlockLocator(32200,
                                                      [Uint256.from_hexstr("000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")]), 
                                         Uint256.zero())
        
        serialized_msg = GetblocksMessageSerializer().serialize(getblocks_msg)
        self.assertEquals(hexstr(serialized_msg), "c87d0000016fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d61900000000000000000000000000000000000000000000000000000000000000000000000000")

    def test_deserialize_getblocks_message(self):
        serialized_getblocks = decodehexstr("c87d0000016fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d61900000000000000000000000000000000000000000000000000000000000000000000000000")
        
        getblocks_msg, _ = GetblocksMessageSerializer().deserialize(serialized_getblocks)
        expected_msg = GetblocksMessage(BlockLocator(32200,
                                                      [Uint256.from_hexstr("000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")]), 
                                         Uint256.zero())
        self.assertEquals(getblocks_msg, expected_msg)

    def test_serialize_getdata_message(self):
        getdata_msg = GetdataMessage([Invitem(INV_TX, Uint256.from_hexstr("72a49ff05829f6c31a089a9c7413498cb18190ffc839208e67a27cc15933a298")),
                                      Invitem(INV_TX, Uint256.from_hexstr("f6eea3dd4f6536350344a535e37a4178170bba18b871a424d696e196d4d3b555")),
                                      Invitem(INV_BLOCK, Uint256.from_hexstr("0000000040a24e14497879bdd67db948cf30edc5d0a5833e8cb2736582157b49"))])
        serialized_msg = GetdataMessageSerializer().serialize(getdata_msg)
        self.assertEquals(hexstr(serialized_msg), "030100000098a23359c17ca2678e2039c8ff9081b18c4913749c9a081ac3f62958f09fa4720100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")

    def test_deserialize_getdata_message(self):
        serialized_getdata = decodehexstr("030100000098a23359c17ca2678e2039c8ff9081b18c4913749c9a081ac3f62958f09fa4720100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")
        getdata_msg, _ = GetdataMessageSerializer().deserialize(serialized_getdata)
        expected_msg = GetdataMessage([Invitem(INV_TX, Uint256.from_hexstr("72a49ff05829f6c31a089a9c7413498cb18190ffc839208e67a27cc15933a298")),
                                      Invitem(INV_TX, Uint256.from_hexstr("f6eea3dd4f6536350344a535e37a4178170bba18b871a424d696e196d4d3b555")),
                                      Invitem(INV_BLOCK, Uint256.from_hexstr("0000000040a24e14497879bdd67db948cf30edc5d0a5833e8cb2736582157b49"))])
        self.assertEquals(getdata_msg, expected_msg)
        
    def test_serialize_getheaders_message(self):
        getheaders_message= GetheadersMessage(BlockLocator(32200, [Uint256.from_hexstr("000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")]), 
                                              Uint256.from_hexstr("72a49ff05829f6c31a089a9c7413498cb18190ffc839208e67a27cc15933a298"))
        serialized_msg = GetheadersMessageSerializer().serialize(getheaders_message)
        self.assertEquals(hexstr(serialized_msg), "c87d0000016fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d619000000000098a23359c17ca2678e2039c8ff9081b18c4913749c9a081ac3f62958f09fa472")

    def test_deserialize_getheaders_message(self):
        serialized_getheaders = decodehexstr("c87d0000016fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d619000000000098a23359c17ca2678e2039c8ff9081b18c4913749c9a081ac3f62958f09fa472")
        getheaders_message, _ = GetheadersMessageSerializer().deserialize(serialized_getheaders)
        expected_message = GetheadersMessage(BlockLocator(32200, [Uint256.from_hexstr("000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")]), 
                                              Uint256.from_hexstr("72a49ff05829f6c31a089a9c7413498cb18190ffc839208e67a27cc15933a298"))
        self.assertEquals(getheaders_message, expected_message)

    def test_serialize_inv_message(self):
        inv_message = InvMessage([Invitem(INV_TX, Uint256.from_hexstr("f6eea3dd4f6536350344a535e37a4178170bba18b871a424d696e196d4d3b555")),
                                  Invitem(INV_BLOCK, Uint256.from_hexstr("0000000040a24e14497879bdd67db948cf30edc5d0a5833e8cb2736582157b49"))])
        serialized_msg = InvMessageSerializer().serialize(inv_message)
        self.assertEquals(hexstr(serialized_msg), "020100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")

    def test_deserialize_inv_message(self):
        serialized_inv_message = decodehexstr("020100000055b5d3d496e196d624a471b818ba0b1778417ae335a544033536654fdda3eef602000000497b15826573b28c3e83a5d0c5ed30cf48b97dd6bd797849144ea24000000000")
        inv_message, _ = InvMessageSerializer().deserialize(serialized_inv_message)
        expected_message = InvMessage([Invitem(INV_TX, Uint256.from_hexstr("f6eea3dd4f6536350344a535e37a4178170bba18b871a424d696e196d4d3b555")),
                                       Invitem(INV_BLOCK, Uint256.from_hexstr("0000000040a24e14497879bdd67db948cf30edc5d0a5833e8cb2736582157b49"))])
        self.assertEquals(inv_message, expected_message)

    def test_serialize_ping_message(self):
        ping_message = PingMessage()
        serialized_msg = PingMessageSerializer().serialize(ping_message)
        self.assertEquals(hexstr(serialized_msg), "")

    def test_deserialize_ping_message(self):
        ping_message = PingMessageSerializer().deserialize("")
        self.assertEquals(ping_message, PingMessage())

    def test_serialize_tx_message(self):
        # TX 1 from block 389 on testnet 3
        tx_message = TxMessage(Tx(version=1, 
                                in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("f519f238c54e20bb418bb4513ce75484546d198200a901be55152e12cfa82652"),index=1), 
                                   script=Script(instructions=[Instruction(73,  decodehexstr("3046022100b96e2fd2015bb3fe22c23c712c3ac4a8636d4a78df7d669babd64eaba314c236022100f402d7e3392d1770ce2be0c823eab0122bb83ee0bd65f5de54a1feb53e452eed01")),Instruction(65,  decodehexstr("04c4bee5e6dbb5c1651437cb4386c1515c7776c64535077204c6f24f05a37d04a32bc78beb2193b53b104c9954c44b0ce168bc78efd5f1e1c7db9d6c21b3016599"))]), 
                                   sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("d748009c88abacfbd8d0dafb5552f0700a16f9a35ff41583988d9f70618c1971"),index=0), 
                                   script=Script(instructions=[Instruction(72,  decodehexstr("304502210092e96f4185fc1bb74b4d9c258219dc5ffc71afb43e73ec0e78bdd91bafbe386e022019fc5b3d9602005b61f5dc75e7bd4dde1c19a0700c0a7958503528014d39019101")),Instruction(33,  decodehexstr("02274eae01d391bbec32d4b60e24d5d24f9cc23ca8da6708cf6c062381bfa71006"))]), 
                                   sequence=4294967295)], 
                                out_list=[TxOut(value=5000000000, 
                                    script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("dbf89509176a975e41d04cc0af24cfc8de4394a9")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)]))], 
                                locktime=0))
        serialized_msg = TxMessageSerializer().serialize(tx_message)
        self.assertEquals(hexstr(serialized_msg), "01000000025226a8cf122e1555be01a90082196d548454e73c51b48b41bb204ec538f219f5010000008c493046022100b96e2fd2015bb3fe22c23c712c3ac4a8636d4a78df7d669babd64eaba314c236022100f402d7e3392d1770ce2be0c823eab0122bb83ee0bd65f5de54a1feb53e452eed014104c4bee5e6dbb5c1651437cb4386c1515c7776c64535077204c6f24f05a37d04a32bc78beb2193b53b104c9954c44b0ce168bc78efd5f1e1c7db9d6c21b3016599ffffffff71198c61709f8d988315f45fa3f9160a70f05255fbdad0d8fbacab889c0048d7000000006b48304502210092e96f4185fc1bb74b4d9c258219dc5ffc71afb43e73ec0e78bdd91bafbe386e022019fc5b3d9602005b61f5dc75e7bd4dde1c19a0700c0a7958503528014d390191012102274eae01d391bbec32d4b60e24d5d24f9cc23ca8da6708cf6c062381bfa71006ffffffff0100f2052a010000001976a914dbf89509176a975e41d04cc0af24cfc8de4394a988ac00000000")

    def test_deserialize_tx_message(self):
        # TX 1 from block 398 on testnet 3
        serialized_tx_message = decodehexstr("010000000328ce10c7189026866bcfc1d06b278981ddf21ec0e364e28e294365b5c328cd43000000006c493046022100b918951cc55fbb285168004de7eab21e702e89dc43c167ba0fc1b09273e29cf5022100f95c24b6c740e2306a45bea1e7a0c8f2032c9d4da4d8d1cc6b5c4166d1fabfe50121033b2dd6fe53611ef3d112b7098a8999f48bf27c7bf94bd045439d87a9ec11fca3fffffffffc4f1ed498c5f31fe90b10389f12566a3350a5080db1dba1f01f8834e5813ca900000000484730440220161ee27efad282e8c984051418fcc2bca6854f3f5d4e24031b950bcd7853943a02202b5566c72aeaff2295db82c79d52d88dbe9450e01c6c951d5d0148c290f6cbbe01fffffffffc5eecfa90d46aeeda36bb1a2f2da61e4f9be81253033ae55625d00acb13ef35000000004a493046022100f7d996bc39ef00b217014ee3e7f8b49ed714fcce2fe970a2ada2b9a87a741c2d022100c55a6089c2b23ec87c5063513c6c8abfc14c913f8ab69cf4ebed6a58c220946901ffffffff0340f1f23a000000001976a914f069756ffd9d331119e5430268437aed14210afb88ac00f2052a0100000017a914290bba32a49315789a030bb40b0047f8fb90ff668700f2052a0100000017a9141d9ca71efa36d814424ea6ca1437e67287aebe348700000000")
        tx_message, _ = TxMessageSerializer().deserialize(serialized_tx_message)
        expected_message = TxMessage(Tx(version=1, 
                in_list=[TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("43cd28c3b56543298ee264e3c01ef2dd8189276bd0c1cf6b86269018c710ce28"),index=0), 
                   script=Script(instructions=[Instruction(73,  decodehexstr("3046022100b918951cc55fbb285168004de7eab21e702e89dc43c167ba0fc1b09273e29cf5022100f95c24b6c740e2306a45bea1e7a0c8f2032c9d4da4d8d1cc6b5c4166d1fabfe501")),Instruction(33,  decodehexstr("033b2dd6fe53611ef3d112b7098a8999f48bf27c7bf94bd045439d87a9ec11fca3"))]), 
                   sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("a93c81e534881ff0a1dbb10d08a550336a56129f38100be91ff3c598d41e4ffc"),index=0), 
                   script=Script(instructions=[Instruction(71,  decodehexstr("30440220161ee27efad282e8c984051418fcc2bca6854f3f5d4e24031b950bcd7853943a02202b5566c72aeaff2295db82c79d52d88dbe9450e01c6c951d5d0148c290f6cbbe01"))]), 
                   sequence=4294967295),TxIn(previous_output=Outpoint(hash=Uint256.from_hexstr("35ef13cb0ad02556e53a035312e89b4f1ea62d2f1abb36daee6ad490faec5efc"),index=0), 
                   script=Script(instructions=[Instruction(73,  decodehexstr("3046022100f7d996bc39ef00b217014ee3e7f8b49ed714fcce2fe970a2ada2b9a87a741c2d022100c55a6089c2b23ec87c5063513c6c8abfc14c913f8ab69cf4ebed6a58c220946901"))]), 
                   sequence=4294967295)], 
                out_list=[TxOut(value=989000000, 
                    script=Script(instructions=[Instruction(OP_DUP),Instruction(OP_HASH160),Instruction(20,  decodehexstr("f069756ffd9d331119e5430268437aed14210afb")),Instruction(OP_EQUALVERIFY),Instruction(OP_CHECKSIG)])),TxOut(value=5000000000, 
                    script=Script(instructions=[Instruction(OP_HASH160),Instruction(20,  decodehexstr("290bba32a49315789a030bb40b0047f8fb90ff66")),Instruction(OP_EQUAL)])),TxOut(value=5000000000, 
                    script=Script(instructions=[Instruction(OP_HASH160),Instruction(20,  decodehexstr("1d9ca71efa36d814424ea6ca1437e67287aebe34")),Instruction(OP_EQUAL)]))], 
                locktime=0))
        self.assertEquals(tx_message, expected_message)

    def test_serialize_verack_message(self):
        verack_message = VerackMessage()
        serialized_msg = VerackMessageSerializer().serialize(verack_message)
        self.assertEquals(hexstr(serialized_msg), "")

    def test_deserialize_verack_message(self):
        verack_message = VerackMessageSerializer().deserialize("")
        self.assertEquals(verack_message, VerackMessage())

    def test_serialize_version_message(self):
        version_message = VersionMessage(version=32200,
                                         services=SERVICES_NODE_NETWORK, 
                                         timestamp=1356475129, 
                                         addr_me=Netaddr(SERVICES_NODE_NETWORK, "213.25.6.223", 2332), 
                                         addr_you=Netaddr(SERVICES_NONE, "68.25.6.32", 8973), 
                                         nonce=16928363815861062023, 
                                         sub_version_num="/coinpy:0.1/", 
                                         start_height=189)
        serialized_msg = VersionMessageSerializer().serialize(version_message)
        self.assertEquals(hexstr(serialized_msg), "c87d00000100000000000000f92ada5000000000010000000000000000000000000000000000ffffd51906df091c000000000000000000000000000000000000ffff44190620230d8789f94033a1edea0c2f636f696e70793a302e312fbd000000")

    def test_deserialize_version_message(self):
        serialized_version_message = decodehexstr("c87d00000100000000000000f92ada5000000000010000000000000000000000000000000000ffffd51906df091c000000000000000000000000000000000000ffff44190620230d8789f94033a1edea0c2f636f696e70793a302e312fbd000000")
        version_message, _ = VersionMessageSerializer().deserialize(serialized_version_message)
        expected_version_message = VersionMessage(version=32200,
                                                  services=SERVICES_NODE_NETWORK, 
                                                  timestamp=1356475129, 
                                                  addr_me=Netaddr(SERVICES_NODE_NETWORK, "213.25.6.223", 2332), 
                                                  addr_you=Netaddr(SERVICES_NONE, "68.25.6.32", 8973), 
                                                  nonce=16928363815861062023, 
                                                  sub_version_num="/coinpy:0.1/", 
                                                  start_height=189)
        self.assertEquals(version_message, expected_version_message)




if __name__ == '__main__':
    unittest.main()
    
