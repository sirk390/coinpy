"""
Created on 13 Jun 2011

@author: kris
"""
from coinpy.model.protocol.messages.types import *

COMMANDS = {MSG_VERSION:"version",
            MSG_VERACK:"verack",
            MSG_ADDR:"addr",
            MSG_INV:"inv",
            MSG_GETDATA:"getdata",
            MSG_GETBLOCKS:"getblocks",
            MSG_GETHEADERS:"getheaders",
            MSG_TX:"tx",
            MSG_BLOCK:"block",
            MSG_HEADERS:"headers",
            MSG_GETADDR:"getaddr",
            MSG_CHECKORDER:"checkorder",
            MSG_SUBMITORDER:"submitorder",
            MSG_REPLY:"reply",
            MSG_PING:"ping",
            MSG_ALERT:"alert"}

COMMANDS_TYPES = dict((name, type) for type, name in COMMANDS.iteritems())
