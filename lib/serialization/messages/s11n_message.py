from coinpy.lib.serialization.magic import MAGICS
from coinpy.lib.serialization.commands import COMMANDS, COMMANDS_TYPES
from coinpy.lib.serialization.common.structure import Structure
from coinpy.lib.serialization.common.field import Field
from coinpy.model.protocol.messages.types import *
from coinpy.lib.serialization.messages.s11n_version import version_encoder
from coinpy.lib.serialization.exceptions import FormatErrorException,\
    MissingDataException
import string
from coinpy.lib.serialization.messages.s11n_verack import verack_encoder
from coinpy.lib.serialization.messages.s11n_inv import inv_encoder
from coinpy.lib.serialization.messages.s11n_getblocks import getblocks_encoder
from coinpy.lib.serialization.messages.s11n_getheaders import getheaders_encoder
from coinpy.lib.serialization.messages.s11n_tx import tx_msg_encoder
from coinpy.lib.serialization.messages.s11n_getdata import getdata_encoder
from coinpy.lib.serialization.messages.s11n_addr import addr_encoder
from coinpy.lib.serialization.messages.s11n_getaddr import getaddr_encoder
from coinpy.model.protocol.messages.getaddr import msg_getaddr
from coinpy.model.protocol.runmode import MAIN
from coinpy.tools.bitcoin.sha256 import sha256checksum
from coinpy.lib.serialization.messages.s11n_block import block_encoder,\
    block_msg_encoder

ENCODERS = {MSG_VERSION: version_encoder(),
            MSG_VERACK: verack_encoder(),
            MSG_ADDR: addr_encoder(),
            MSG_INV: inv_encoder(),
            MSG_GETDATA: getdata_encoder(),
            MSG_GETBLOCKS: getblocks_encoder(),
            MSG_GETHEADERS: getheaders_encoder(),
            MSG_TX: tx_msg_encoder(),
            MSG_BLOCK: block_msg_encoder(),
            MSG_HEADERS: None,
            MSG_GETADDR: getaddr_encoder(),
            MSG_CHECKORDER: None,
            MSG_SUBMITORDER: None,
            MSG_REPLY: None,
            MSG_PING: None,
            MSG_ALERT: None}

class MessageEncoder():
    MESSAGE_HEADER = Structure([Field("<I",  "magic"),
                                Field("12s","command"),
                                Field("<I",  "length")], "message")
    def __init__(self, runmode, log):
        self.runmode= runmode
        self.log = log

    def encode(self, msg):
        if (msg.type not in ENCODERS):
            raise Exception("Encoder not found for type: %d" % (msg.type))
        payload = ENCODERS[msg.type].encode(msg)
        result = self.MESSAGE_HEADER.encode(MAGICS[self.runmode],
                                            COMMANDS[msg.type],
                                            len(payload))
        #MSG_VERSION, MSG_VERACK exception: no checksum
        if (msg.type != MSG_VERSION and msg.type != MSG_VERACK):
            result += sha256checksum(payload)
        result += payload
        return (result)
    
    def decode(self, data, cursor=0):
        result, cursor = self.MESSAGE_HEADER.decode(data, cursor)
        magic, command, length = result
        pos = string.find(command, "\0")
        if (pos != -1):
            command = command[0:pos]
        if (command not in COMMANDS_TYPES):
            raise FormatErrorException("Error: unknown command : %s" % (command))
        if ( ENCODERS[COMMANDS_TYPES[command]] == None):
            raise Exception("Error: Unsupported command : %s" % (command))
        msg_type = COMMANDS_TYPES[command]
        if (msg_type != MSG_VERSION and msg_type != MSG_VERACK):
            checksum = data[cursor:cursor+4]
            cursor += 4
            startplayload = cursor 
                #raise FormatErrorException("Checksum error in command: %s %s != %s" % (command, hexdump1(checksum,""), hexdump1(verify,"")))
             
        if (magic != MAGICS[self.runmode]):
            raise FormatErrorException("Error: wrong magic : expected:%s received:%s" % (MAGICS[self.runmode], magic))
        if (len(data) - cursor < length):
            raise MissingDataException("Command incomplete: %s" % (command))
        #self.log.debug("Decoding: %s" % (command))
        res, cursor = ENCODERS[COMMANDS_TYPES[command]].decode(data, cursor)
        #verify checksum after decoding (required to identify message boundaries)
        if (msg_type != MSG_VERSION and msg_type != MSG_VERACK):
            verify = sha256checksum(data[startplayload:cursor])
            if (checksum != verify):
                #raise FormatErrorException("Checksum error in command: %s %s != %s" % (command, hexdump1(checksum,""), hexdump1(verify,"")))
                self.log.warning( "Checksum error in command: %s %s != %s" % (command, hexdump1(checksum,""), hexdump1(verify,"")))
        return (res, cursor)  

if __name__ == '__main__':
    from coinpy.model.protocol.services import SERVICES_NONE
    from coinpy.model.protocol.structures.netaddr import netaddr
    from coinpy.model.protocol.messages.version import msg_version
    import time
    addr_me = netaddr(1, "192.168.1.29", 4865)
    addr_you = netaddr(SERVICES_NONE, "192.168.1.30", 879)
    vermsg = msg_version(version = 209, 
                         services=SERVICES_NONE, 
                         timestamp=time.time(), 
                         addr_me=addr_me, 
                         addr_you=addr_you, 
                         nonce=789, 
                         sub_version_num="mybitcoin",
                         start_height=100)
    data = MessageEncoder(MAIN).encode(vermsg)
    
    data2 = MessageEncoder(MAIN).encode(msg_getaddr())
    
    print hexdump1(data2)
    
    
    
    