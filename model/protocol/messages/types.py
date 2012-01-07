MSG_VERSION, MSG_VERACK, MSG_ADDR, MSG_INV, MSG_GETDATA, \
MSG_GETBLOCKS, MSG_GETHEADERS, MSG_TX, MSG_BLOCK, \
MSG_HEADERS, MSG_GETADDR, MSG_CHECKORDER, MSG_SUBMITORDER, \
MSG_REPLY, MSG_PING, MSG_ALERT \
    = MESSAGE_TYPES = range(16)

MESSAGE_NAMES = \
{
    MSG_VERSION : "version", 
    MSG_VERACK : "verack", 
    MSG_ADDR : "addr", 
    MSG_INV : "inv", 
    MSG_GETDATA : "getdata",
    MSG_GETBLOCKS : "blocks", 
    MSG_GETHEADERS : "headers", 
    MSG_TX : "tx", 
    MSG_BLOCK : "block",
    MSG_HEADERS : "headers", 
    MSG_GETADDR : "getaddr", 
    MSG_CHECKORDER : "checkorder", 
    MSG_SUBMITORDER : "submitorder", 
    MSG_REPLY : "reply", 
    MSG_PING : "ping", 
    MSG_ALERT : "alert"
}