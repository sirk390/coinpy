import asyncore
import socket
import traceback
from coinpy.tools.observer import Observable

class PeerHandler(asyncore.dispatcher_with_send, Observable):
    EVT_CONNECT = Observable.createevent()
    EVT_DISCONNECT = Observable.createevent()
   
    def __init__(self, reactor, sockaddr, sock=None):
        Observable.__init__(self, reactor)
        asyncore.dispatcher_with_send.__init__(self, sock=sock)
        self.sockaddr = sockaddr
        self.isoutbound = (sock == None)
        if not sock:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect((sockaddr.ip, sockaddr.port))
                
    def handle_connect(self):
        self.fire(self.EVT_CONNECT)
 
    def handle_error(self):
        traceback.print_exc()
            
    def handle_close(self):
        self.fire(self.EVT_DISCONNECT)
        self.close()
        
    def __str__(self):
        return str(self.sockaddr)
