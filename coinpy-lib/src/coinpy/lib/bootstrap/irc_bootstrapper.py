import random
import struct
from coinpy.tools.bitcoin.base58check import decode_base58check
from coinpy.tools.observer import Observable
from coinpy.lib.bootstrap.irc_handler import IrcHandler
from coinpy.model.protocol.runmode import MAIN
from coinpy.node.network.sockaddr import SockAddr

class IrcBootstrapper(Observable):
    EVT_FOUND_PEER = Observable.createevent()
    
    def __init__(self, runmode, log, ircserver=SockAddr("92.243.23.21", 6667)):#irc.lfnet.org
        super(IrcBootstrapper, self).__init__()
        self.log = log
        self.runmode = runmode
        self.ircserver = ircserver
        self.running = False
        self.irc_handler = None
        
    def start(self):
        if (not self.running):
            self.running = True
            self.irc_handler = IrcHandler(self.log, self.ircserver)
            self.irc_handler.subscribe(IrcHandler.EVT_CONNECT, self.on_irc_connected)
            self.irc_handler.subscribe(IrcHandler.EVT_RECV_LINE, self.on_irc_recv_line)
            self.irc_handler.subscribe(IrcHandler.EVT_DISCONNECT, self.on_irc_disconnected)
            
    def on_irc_connected(self, event):
        self.log.info("Connected to irc server : %s" % (str(self.ircserver)))
        channel = (self.runmode == MAIN) and '#bitcoin' or '#bitcoinTEST'
        name = "x%u" % random.randint(0, 1000000000) 
        self.irc_handler.send('NICK %s\r\n' % name)
        self.irc_handler.send('USER %s 8 * %s\r\n' % (name,name))
        self.irc_handler.send("JOIN " +  channel + "\r\n")
        self.irc_handler.send("WHO " +  channel + "\r\n")
        
    def on_irc_disconnected(self, event):
        self.log.info("Disconnected from irc server : %s" % (str(self.ircserver)))
        self.running = False
        self.irc_handler = None
        
    def on_irc_recv_line(self, event):
        tokens = event.line.split(" ")
        if (tokens[1] == "352"):
            self.found_nick(tokens[7])
        if (tokens[1] == "315"):
            self.stop()

    def found_nick(self, nick):
        if nick[0] == 'u': #routable 
            try:
                hostaddr = decode_base58check(nick[1:])
                ip = ".".join([str(struct.unpack(">B", x)[0]) for x in hostaddr[:4]])
                port = struct.unpack(">H", hostaddr[4:])[0]
            except:
                self.log.info("Error unpacking nickname (errorneous peer): %s" % (nick))
                return
            self.fire(self.EVT_FOUND_PEER, peeraddress=SockAddr(ip, port))
            
    def stop(self):
        if (self.running):
            self.irc_handler.handle_close()


