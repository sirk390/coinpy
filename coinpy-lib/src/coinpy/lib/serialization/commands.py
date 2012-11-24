from coinpy.model.protocol.messages.types import MSG_VERSION, MSG_VERACK, MSG_ADDR,\
    MSG_INV, MSG_GETDATA, MSG_GETBLOCKS, MSG_GETHEADERS, MSG_TX, MSG_BLOCK,\
    MSG_HEADERS, MSG_GETADDR, MSG_CHECKORDER, MSG_SUBMITORDER, MSG_REPLY,\
    MSG_PING, MSG_ALERT

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
